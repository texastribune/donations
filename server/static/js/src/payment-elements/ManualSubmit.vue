<template>
  <input
    :class="classes"
    :value="value"
    :disabled="isFetchingToken"
    type="submit"
    @click="onClick"
  />
</template>

<script>
import Vue from 'vue';
import { createToken } from 'vue-stripe-elements-plus';

import getRecaptchaToken from '../utils/get-recaptcha-token';
import { RecaptchaError, StripeError } from '../errors';
import { RECAPTCHA_ERROR_MESSAGE } from '../constants';

const CARD_ERROR_MESSAGE =
  'There was an issue processing your card. Please try a different card and submit the form again. If the issue persists, contact inquiries@texastribune.org.';

export default {
  name: 'ManualSubmit',

  props: {
    value: {
      type: String,
      default: 'Submit',
    },

    formIsValid: {
      type: Boolean,
      required: true,
    },

    isFetchingToken: {
      type: Boolean,
      required: true,
    },
  },

  methods: {
    markFetchingToken() {
      this.$emit('setLocalValue', { key: 'isFetchingToken', value: true });
    },

    markNotFetchingToken() {
      this.$emit('setLocalValue', { key: 'isFetchingToken', value: false });
    },

    async onClick() {
      this.$emit('setLocalValue', [
        { key: 'showErrors', value: true },
        { key: 'serverErrorMessage', value: '' },
        { key: 'genericErrorMessage', value: '' },
      ]);

      this.$emit('setCardValue', { key: 'showError', value: true });

      if (this.formIsValid) {
        this.markFetchingToken();

        try {
          let recaptchaToken;

          try {
            recaptchaToken = await getRecaptchaToken('manualPay');
          } catch (err) {
            throw new RecaptchaError();
          }

          this.$emit('setLocalValue', {
            key: 'recaptchaToken',
            value: recaptchaToken,
          });

          const stripeResult = await createToken();

          if (stripeResult.error) {
            const { message, type } = stripeResult.error;
            throw new StripeError(message, type);
          }

          this.$emit('setLocalValue', {
            key: 'stripeToken',
            value: stripeResult.token.id,
          });

          Vue.nextTick(() => {
            this.$emit('onSubmit');
          });
        } catch (error) {
          this.markNotFetchingToken();

          if (error instanceof RecaptchaError) {
            this.$emit('setLocalValue', {
              key: 'genericErrorMessage',
              value: RECAPTCHA_ERROR_MESSAGE,
            });
          } else if (error instanceof StripeError) {
            let messageToShow;

            if (error.type === 'validation_error') {
              messageToShow = error.message;
            } else {
              messageToShow = CARD_ERROR_MESSAGE;
            }

            this.$emit('setCardValue', [
              { key: 'isValid', value: false },
              { key: 'errorMessage', value: messageToShow },
            ]);
          }
        }
      }
    },
  },
};
</script>
