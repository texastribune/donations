<template>
  <div
    :class="classesWithValidation"
  >
    <card
      :options="options"
      :stripe="stripeKey"
      @change="onChange"
    />
    <p
      v-if="showError && !valid"
      role="alert"
    >
      {{ errorMessage }}
    </p>
  </div>
</template>

<script>
import { Card } from 'vue-stripe-elements-plus';

import updateValidity from './mixins/updateValidity';

export default {
  name: 'ManualPay',

  components: {
    Card,
  },

  mixins: [updateValidity],

  props: {
    showError: {
      type: Boolean,
      default: false,
    },

    validation: {
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

    valid() {
      return this.validation.valid;
    },

    errorMessage() {
      return this.validation.message;
    },

    classesWithValidation() {
      const { classes } = this;
      if (!this.showError || this.valid) return classes;
      return `invalid ${classes}`;
    },
  },

  methods: {
    onChange({ error, empty }) {
      if (error) {
        this.markMessageAndInvalid({ element: 'card', message: error.message });
      } else if (empty) {
        this.markMessageAndInvalid({ element: 'card', message: 'Your card number is incomplete' });
      } else {
        this.markValid('card');
      }
    },
  },
};
</script>
