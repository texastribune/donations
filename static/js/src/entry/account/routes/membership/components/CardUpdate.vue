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
import store from '../../../store';
import { ValidationObserver } from 'vee-validate';
import { createToken } from 'vue-stripe-elements-plus';
import userMixin from '../../../store/user/mixin';
import { USER_MODULE, USER_TYPES } from '../../../store/types';
import ManualPay from '../../../../../payment-elements/ManualPay.vue';
import formStarter from '../../../../../mixins/connected-form/starter';

export default {
  name: 'CardUpdate',

  components: {
    ManualPay,
    ValidationObserver,
  },

  mixins: [formStarter, userMixin],

  data() {
    return {
      openPaymentForm: false,
      formSubmitted: false,
    };
  },

  methods: {
    async patchCard() {
      this.formSubmitted = true;
      await createToken().then(data => {
        const newCard = data.token.card

        this[USER_TYPES.updateCreditCard]({
          card: data.token.id,
          last4: newCard.last4,
          year: newCard.exp_year,
          month: newCard.exp_month,
          brand: newCard.brand
        });
        // store.dispatch(`${USER_MODULE}/${USER_TYPES.getUser}`);
        const successMessage = `Card ending in ${newCard.last4}, expiring ${newCard.exp_month}/${newCard.exp_year} has been saved`;
        this.$emit(
          'onSuccess',
          successMessage,
          newCard.last4,
          newCard.brand
        );
      });

    },
  },
}
</script>