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

export default {
  name: 'CardPay',

  components: {
    Card,
  },

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
          this.$store.dispatch(
            `${this.tokenStoreModule}/updateValue`,
            { key: 'stripeToken', value: id },
          );
          this.$emit('markErrorValidity', 'stripeToken', true);
        }).catch(() => {
          window.location.href = '/error';
        });
      } else {
        this.$store.dispatch(
          `${this.tokenStoreModule}/updateValue`,
          { key: 'stripeToken', value: '' },
        );
        this.$emit('markErrorValidity', 'stripeToken', false);
      }
    },
  },
};
</script>
