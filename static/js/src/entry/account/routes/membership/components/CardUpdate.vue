<template>
  <transition name="has-fade">
    <section class="c-detail-box">
      <validation-observer v-slot="{ handleSubmit }">
        <form @submit.prevent="handleSubmit(patchCard)">
          <manual-pay
            :card="card"
            base-classes="form__manual"
            @setCardValue="setCardValue"
          />
          <button
            class="c-button c-button--s has-text-white has-bg-teal l-width-full l-display-block"
            :disabled="!card.isValid"
          >
            Save
          </button>
        </form>
      </validation-observer>
    </section>
  </transition>
</template>

<script>
import { ValidationObserver } from 'vee-validate';
import { createToken } from 'vue-stripe-elements-plus';
import userMixin from '../../../store/user/mixin';
import contextMixin from '../../../store/context/mixin';
import { CONTEXT_TYPES, USER_TYPES } from '../../../store/types';
import ManualPay from '../../../../../payment-elements/ManualPay.vue';
import logError from '../../../utils/log-error';
import formStarter from '../../../../../mixins/connected-form/starter';

export default {
  name: 'CardUpdate',

  components: {
    ManualPay,
    ValidationObserver,
  },

  mixins: [formStarter, contextMixin, userMixin],

  data() {
    return {
      openPaymentForm: false,
      formSubmitted: false,
      stripeTokenId: '',
      stripeCard: {},
      badCard: false,
      errMessage: {},
    };
  },

  methods: {
    async patchCard() {
      this.$emit(
        'formSubmitted'
      )
      this[CONTEXT_TYPES.setIsFetching](true);
      this.formSubmitted = true;
      await createToken().then(data => {
        this.stripeTokenId = data.token.id;
        this.stripeCard = data.token.card;
      });
      // waiting on this one so we can see if the card is declined
      await this.updateStripe();
      if (!this.badCard) {
        // opportunities in salesforce can update in the background and log any errors
        this.updateSalesforce();
        const successMessage = `Card ending in ${this.stripeCard.last4}, expiring ${this.stripeCard.exp_month}/${this.stripeCard.exp_year} has been saved`;
        this.$emit(
          'onSuccess',
          successMessage
        );
      }
      this[CONTEXT_TYPES.setIsFetching](false);
    },

    async updateStripe() {
      this.badCard = false;
      try {
        await this[USER_TYPES.updateCard]({
          tokenId: this.stripeTokenId,
          card: this.stripeCard,
        });
      } catch (err) {
        this.badCard = true;
        this.$emit(
          'badCard',
          true,
        )
        logError({err, level: 'warning'})

      }
    },
    updateSalesforce() {
      this[USER_TYPES.updateOpportunities]({
        last4: this.stripeCard.last4,
        year: this.stripeCard.exp_year,
        month: this.stripeCard.exp_month,
        brand: this.stripeCard.brand
      });
    }
  },
}
</script>