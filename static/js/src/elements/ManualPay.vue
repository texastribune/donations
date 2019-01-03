<template>
  <div :class="classesWithValidation">
    <card :options="options" :stripe="stripeKey" @change="onChange" />
    <p v-if="showError && !isValid" role="alert">{{ message }}</p>
  </div>
</template>

<script>
import { Card } from 'vue-stripe-elements-plus';

export default {
  name: 'ManualPay',

  components: {
    Card,
  },

  props: {
    showError: {
      type: Boolean,
      default: false,
    },

    card: {
      type: Object,
      required: true,
    },
  },

  data() {
    return {
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

    isValid() {
      return this.card.isValid;
    },

    message() {
      return this.card.message;
    },

    classesWithValidation() {
      const { classes } = this;
      if (!this.showError || this.isValid) return classes;
      return `invalid ${classes}`;
    },
  },

  methods: {
    onChange({ error, empty }) {
      let validValue;
      let messageValue;

      if (error) {
        validValue = false;
        messageValue = error.message;
      } else if (empty) {
        validValue = false;
        messageValue = 'Your card number is incomplete';
      } else {
        validValue = true;
        messageValue = '';
      }

      this.$emit('setCardValue', [
        { key: 'isValid', value: validValue },
        { key: 'message', value: messageValue },
      ]);
    },
  },
};
</script>
