<template>
  <div
    v-show="supported"
    :class="classes"
  >
    <div
      ref="native"
    />
    <p>
      <a
        href
        role="button"
        @keypress.space="$event.preventDefault"
        @click="showManual"
        @keyup.space="showManual"
      >
        Or enter credit card manually
      </a>
    </p>
  </div>
</template>

<script>
/* global Stripe */

import Vue from 'vue';

export default {
  name: 'NativePay',

  props: {
    supported: {
      type: Boolean,
      required: true,
    },

    amountStoreModule: {
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
      const getter =
        this.$store.getters[`${this.amountStoreModule}/valueByKey`];
      const amountInDollars = parseFloat(getter('amount'));
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

  mounted() {
    this.buildNativePayment();
  },

  methods: {
    buildNativePayment() {
      // eslint-disable-next-line no-underscore-dangle
      const stripe = new Stripe(window.__STRIPE_KEY__);
      const paymentRequest = stripe.paymentRequest({
        country: 'US',
        currency: 'usd',
        total: {
          label: 'Texas Tribune Donation',
          amount: this.amount,
        },
      });
      const button =
        stripe.elements().create('paymentRequestButton', {
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
        .then((result) => {
          if (result) {
            this.$emit('setValue', { key: 'nativeIsSupported', value: true });
            button.mount(this.$refs.native);
          } else {
            throw new Error();
          }
        })
        .catch(() => {
          this.$emit('setValue', { key: 'showManualPay', value: true });
        });

      button.on('click', (event) => {
        const updates = [
          { key: 'showManualErrors', value: false },
          { key: 'showNativeErrors', value: true },
          { key: 'serverErrorMessage', value: '' },
        ];

        this.$emit('setValue', updates);
        if (!this.formIsValid) event.preventDefault();
      });

      paymentRequest.on('token', (event) => {
        const { token: { id } } = event;

        this.$emit('setValue', {
          key: 'stripeToken',
          value: id,
        });

        event.complete('success');
        Vue.nextTick(() => { this.$emit('onSubmit'); });
      });
    },

    showManual(event) {
      event.preventDefault();
      this.$emit('setValue', { key: 'showManualPay', value: true });
    },
  },
};
</script>
