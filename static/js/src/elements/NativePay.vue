<template>
  <div>
    <div
      v-show="supported"
      ref="native"
    />
  </div>
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
      return getter('amount');
    },
  },

  watch: {
    amount(newAmount, oldAmount) {
      if (newAmount !== oldAmount) {
        const total = {
          label: 'Texas Tribune Donation',
          amount: this.amount * 100,
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
          amount: this.amount * 100,
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
