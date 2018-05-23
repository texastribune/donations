<template>
  <div
    :class="getClasses({ elName: 'container' })"
  >
    <card
      :options="options"
      :class="cardClassesWithValidation"
      :stripe="stripeKey"
      @change="onChange($event.complete)"
    />
    <p
      v-if="showError && !valid"
      :class="getClasses({ elName: 'error' })"
    >
      {{ errorMessage }}
    </p>
  </div>
</template>

<script>
import { Card, createToken } from 'vue-stripe-elements-plus';

import updateStoreValue from './mixins/updateStoreValue';

export default {
  name: 'ManualPay',

  components: {
    Card,
  },

  mixins: [updateStoreValue],

  props: {
    containerClasses: {
      type: String,
      default: '',
    },

    cardClasses: {
      type: String,
      default: '',
    },

    errorClasses: {
      type: String,
      default: '',
    },

    showError: {
      type: Boolean,
      default: false,
    },

    tokenStoreModule: {
      type: String,
      required: true,
    },

    validation: {
      type: Object,
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

    valid() {
      return this.validation.valid;
    },

    errorMessage() {
      return this.validation.message;
    },

    cardClassesWithValidation() {
      const classes = this.getClasses({ elName: 'card' });
      if (!this.showError || this.valid) return classes;
      return `invalid ${classes}`;
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
