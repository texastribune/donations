<template>
  <modal
    :max-width="450"
    :click-to-close="false"
    name="cardModal"
    width="80%"
    height="auto"
    adaptive
  >
    <div class="c-modal">
      <div class="c-modal__heading l-align-center-children">
        <h3 class="t-size-b t-align-center t-lh-b has-text-gray-dark">Update Payment Info</h3>
      </div>
      <validation-observer v-slot="{ handleSubmit }">
        <form @submit.prevent="handleSubmit(patchCard)">
          <manual-pay
            class="c-modal__body"
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
    </div>
    <button
      class="c-modal__close has-bg-white has-text-gray"
      aria-label="close modal"
      @click="$emit('onClose')"
    >
      <icon name="close" :display="{ size: 'xxs', color: 'gray' }" />
    </button>
  </modal>
</template>

<script>
import { ValidationObserver } from 'vee-validate';
import { createToken } from 'vue-stripe-elements-plus';

import { CONTEXT_TYPES, USER_TYPES } from '../../../store/types';
import userMixin from '../../../store/user/mixin';
import contextMixin from '../../../store/context/mixin';

import ManualPay from '../../../../../payment-elements/ManualPay.vue';
import formStarter from '../../../../../mixins/connected-form/starter';

import { AxiosError } from '../../../errors';
import logError from '../../../utils/log-error';

export default {
  name: 'CardUpdate',

  components: {
    ManualPay,
    ValidationObserver,
  },

  mixins: [formStarter, contextMixin, userMixin],

  props: {
    rdo: {
      type: Object,
      required: true,
    }
  },

  data() {
    return {
      stripeTokenId: '',
      stripeCard: {},
      updateFailure: false,
    };
  },

  methods: {
    async patchCard() {
      this[CONTEXT_TYPES.setIsFetching](true);
      await createToken().then(data => {
        this.stripeTokenId = data.token.id;
        this.stripeCard = data.token.card;
      });
      // waiting on this one so we can see if the card is declined
      await this.updateStripe();
      if (!this.updateFailure) {
        // opportunities in salesforce can update in the background and log any errors
        await this.updateSalesforce();
        const successMessage = `Card ending in <b>${this.stripeCard.last4}</b>, expiring ${this.stripeCard.exp_month}/${this.stripeCard.exp_year} has been saved \
          for your ${this.rdo.period} donation of $${this.rdo.amount}`;
        this.$emit(
          'onSuccess',
          successMessage
        );
      }
      this[CONTEXT_TYPES.setIsFetching](false);
    },

    async updateStripe() {
      this.updateFailure = false;

      try {
        await this[USER_TYPES.updateCard]({
          tokenId: this.stripeTokenId,
          card: this.stripeCard,
          stripeCustomerId: this.rdo.stripe_customer_id,
        });
      } catch (err) {
        this.updateFailure = true;
        logError({err, level: 'warning'})

        if (
          err instanceof AxiosError &&
          err.status === 400
        ) {
          if (
            err.extra.data.detail === "missing data"
          ) {
            this.$emit(
              'onFailure',
              'An internal error occurred. Please try again and if the issue persists, contact us at membership@texastribune.org',
            )
          }
          else if (
            err.extra.data.detail === "invalid card"
          ) {
            this.$emit(
              'onFailure',
              'The submitted card was declined or invalid. Please check your information and resubmit'
            )
          }
        }
      }
    },

    async updateSalesforce() {
      await this[USER_TYPES.updateRdoCard]({
        rdoId: this.rdo.id,
        card: {
          last4: this.stripeCard.last4,
          year: this.stripeCard.exp_year,
          month: this.stripeCard.exp_month,
          brand: this.stripeCard.brand,
        }
      });
    }
  },
}
</script>