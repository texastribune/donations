<template>
  <div v-show="supported" :class="classes">
    <div ref="native" />
    <p>
      <a
        href
        role="button"
        @keypress.space="$event.preventDefault"
        @click="showManual"
        @keyup.space="showManual"
        >Or enter credit card manually</a
      >
    </p>
  </div>
</template>

<script>
/* global Stripe */

import Vue from 'vue';

import getRecaptchaToken from '../utils/get-recaptcha-token';
import { RECAPTCHA_ERROR_MESSAGE, STRIPE_KEY } from '../constants';

export default {
  name: 'NativePay',

  props: {
    supported: {
      type: Boolean,
      required: true,
    },

    storeModule: {
      type: String,
      required: true,
    },

    formIsValid: {
      type: Boolean,
      required: true,
    },
  },

  computed: {
    amount() {
      const getter = this.$store.getters[`${this.storeModule}/valueByKey`];
      let amount = getter('amount');

      if (amount.charAt(0) === '$') {
        amount = amount.substring(1);
      }

      const amountInDollars = parseFloat(amount.trim());
      const roundedAmountInCents = (amountInDollars * 100).toFixed();

      return Number(roundedAmountInCents);
    },
  },

  watch: {
    amount(newAmount) {
      // eslint-disable-next-line no-restricted-globals
      const isNumeric = !isNaN(parseFloat(newAmount));

      if (isNumeric) {
        const total = {
          label: 'Texas Tribune Donation',
          amount: newAmount,
        };

        this.paymentRequest.update({ total });
      }
    },
  },

  created() {
    this.buildNativePayment();
  },

  methods: {
    buildNativePayment() {
      // eslint-disable-next-line no-underscore-dangle
      const stripe = new Stripe(STRIPE_KEY);
      const paymentRequest = stripe.paymentRequest({
        country: 'US',
        currency: 'usd',
        total: {
          label: 'Texas Tribune Donation',
          amount: this.amount,
        },
      });
      const button = stripe.elements().create('paymentRequestButton', {
        paymentRequest,
        style: {
          paymentRequestButton: {
            type: 'donate',
          },
        },
      });

      this.paymentRequest = paymentRequest;

      paymentRequest
        .canMakePayment()
        .then(result => {
          if (result) {
            this.$emit('setLocalValue', {
              key: 'nativeIsSupported',
              value: true,
            });

            button.mount(this.$refs.native);
          } else {
            throw new Error();
          }
        })
        .catch(() => {
          this.$emit('setLocalValue', { key: 'showManualPay', value: true });
        });

      button.on('click', event => {
        this.$emit('setLocalValue', [
          { key: 'showErrors', value: true },
          { key: 'serverErrorMessage', value: '' },
          { key: 'genericErrorMessage', value: '' },
        ]);

        this.$emit('setCardValue', { key: 'showError', value: false });

        if (!this.formIsValid) event.preventDefault();
      });

      paymentRequest.on('token', async event => {
        const {
          token: { id },
        } = event;

        try {
          const recaptchaToken = await getRecaptchaToken('nativePay');

          this.$emit('setLocalValue', [
            { key: 'stripeToken', value: id },
            { key: 'recaptchaToken', value: recaptchaToken },
          ]);

          event.complete('success');

          Vue.nextTick(() => {
            this.$emit('onSubmit');
          });
        } catch (err) {
          this.$emit('setLocalValue', {
            key: 'genericErrorMessage',
            value: RECAPTCHA_ERROR_MESSAGE,
          });

          event.complete('fail');
        }
      });
    },

    showManual(event) {
      event.preventDefault();
      this.$emit('setLocalValue', { key: 'showManualPay', value: true });
    },
  },
};
</script>
