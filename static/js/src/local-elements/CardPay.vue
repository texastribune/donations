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
    tokenFieldName: {
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
          this.$emit('setValue', 'token', id);
          this.$emit('markValidity', this.tokenFieldName, true);
        }).catch(() => {
          window.location.href = '/error';
        });
      } else {
        this.$emit('setValue', 'token', '');
        this.$emit('markValidity', this.tokenFieldName, false);
      }
    },
  },
};
</script>
