<template>
  <div>
    <card
      :options="options"
      :class="classes"
      :stripe="stripeKey"
      @change="onChange($event.complete)"
    />
    <p
      v-if="showError && !valid"
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
