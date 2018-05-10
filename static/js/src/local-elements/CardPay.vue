<template>
  <card
    :options="options"
    class="donation--card"
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
          this.$emit('setToken', id);
        }).catch(() => {
          window.location.href = '/error';
        });
      } else {
        this.$emit('setToken', '');
      }
    },
  },
};
</script>
