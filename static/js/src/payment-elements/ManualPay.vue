<template>
  <div :class="classesWithValidation">
    <card :options="options" :stripe="stripeKey" @change="onChange" />
    <p v-if="showError && !isValid" role="alert">{{ message }}</p>
  </div>
</template>

<script>
import { Card } from 'vue-stripe-elements-plus';

import { STRIPE_KEY } from '../constants';

export default {
  name: 'ManualPay',

  components: {
    Card,
  },

  props: {
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
      return STRIPE_KEY;
    },

    isValid() {
      return this.card.isValid;
    },

    showError() {
      return this.card.showError;
    },

    message() {
      return this.card.errorMessage;
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
        { key: 'errorMessage', value: messageValue },
      ]);
    },
  },
};
</script>
