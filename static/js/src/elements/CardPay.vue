<template>
  <card
    :options="options"
    :class="getCssClasses()"
    stripe="pk_test_sSUhBbATSHteQVZZvz6R5aYe"
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

  methods: {
    onChange(isComplete) {
      if (isComplete) {
        createToken().then(({ token: { id } }) => {
          this.updateStoreValue({
            storeModule: this.tokenStoreModule,
            key: 'stripeToken',
            value: id,
          });
          this.$emit('markErrorValidity', 'stripeToken', true);
        }).catch(() => {
          window.location.href = '/error';
        });
      } else {
        this.$emit('markErrorValidity', 'stripeToken', false);
      }
    },
  },
};
</script>
