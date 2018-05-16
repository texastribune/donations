<template>
  <card
    :options="options"
    :class="classes"
    :stripe="stripeKey"
    @change="onChange($event.complete)"
  />
</template>

<script>
import { Card, createToken } from 'vue-stripe-elements-plus';

import updateStoreValue from './mixins/updateStoreValue';

export default {
  name: 'CardPay',

  components: {
    Card,
  },

  mixins: [updateStoreValue],

  props: {
    tokenStoreModule: {
      type: String,
      required: true,
    },
  },

  data() {
    return {
      complete: false,
      options: {
        hidePostalCode: true,
        iconStyle: 'solid',
      },
    };
  },

  computed: {
    stripeKey() {
      // eslint-disable-next-line no-underscore-dangle
      return window.__STRIPE_KEY__;
    },
  },

  methods: {
    onChange(isComplete) {
      if (isComplete) {
        createToken().then(({ token: { id } }) => {
          this.updateStoreValue({
            storeModule: this.tokenStoreModule,
            key: 'stripeToken',
            value: id,
          });

          this.$emit('markErrorValidity', { key: 'card', isValid: true });
        }).catch(() => {
          window.location.href = '/error';
        });
      } else {
        this.$emit('markErrorValidity', { key: 'card', isValid: false });
      }
    },
  },
};
</script>
