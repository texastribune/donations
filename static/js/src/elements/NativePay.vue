<template>
  <div
    v-show="supported"
    ref="native"
  />
</template>

<script>
/* global Stripe */

import Vue from 'vue';

import updateStoreValue from './mixins/updateStoreValue';

export default {
  name: 'NativePay',

  mixins: [updateStoreValue],

  props: {
    amountStoreModule: {
      type: String,
      required: true,
    },

    tokenStoreModule: {
      type: String,
      required: true,
    },

    valid: {
      type: Boolean,
      required: true,
    },
  },

  data() {
    return {
      supported: false,
    };
  },

  computed: {
    amount() {
      const getter =
        this.$store.getters[`${this.amountStoreModule}/valueByKey`];
      return parseFloat(getter('amount')).toFixed(2) * 100;
    },
  },

  watch: {
    amount(newAmount, oldAmount) {
      if (newAmount !== oldAmount) {
        const total = {
          label: 'Texas Tribune Donation',
          amount: this.amount,
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
      const stripe = new Stripe('pk_test_sSUhBbATSHteQVZZvz6R5aYe');
      const paymentRequest = stripe.paymentRequest({
        country: 'US',
        currency: 'usd',
        total: {
          label: 'Texas Tribune Donation',
          amount: this.amount,
        },
      });
      const button =
        stripe.elements().create('paymentRequestButton', { paymentRequest });

      this.paymentRequest = paymentRequest;

      paymentRequest
        .canMakePayment()
        .then((result) => {
          if (result) {
            this.supported = true;
            button.mount(this.$refs.native);
          }
        })
        .catch(() => {});

      button.on('click', (event) => {
        this.$emit('setValue', { key: 'showCardErrors', value: false });
        this.$emit('setValue', { key: 'showNativeErrors', value: true });
        if (!this.valid) event.preventDefault();
      });

      paymentRequest.on('token', (event) => {
        this.updateStoreValue({
          storeModule: this.tokenStoreModule,
          key: 'stripeToken',
          value: event.token.id,
        });
        event.complete('success');
        Vue.nextTick(() => { this.$emit('onSubmit'); });
      });
    },
  },
};
</script>
