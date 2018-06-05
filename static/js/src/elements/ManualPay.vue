<template>
  <div
    :class="classesWithValidation"
  >
    <card
      :options="options"
      :stripe="stripeKey"
      @change="onChange($event.complete)"
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
import { Card, createToken } from 'vue-stripe-elements-plus';

import updateStoreValue from './mixins/updateStoreValue';
import getStoreValue from './mixins/getStoreValue';
import createCustomerOnServer from './mixins/createCustomerOnServer';

export default {
  name: 'ManualPay',

  components: {
    Card,
  },

  mixins: [
    updateStoreValue,
    getStoreValue,
    createCustomerOnServer,
  ],

  props: {
    errorClasses: {
      type: String,
      default: '',
    },

    showError: {
      type: Boolean,
      default: false,
    },

    customerIdStoreModule: {
      type: String,
      required: true,
    },

    emailStoreModule: {
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

    classesWithValidation() {
      const { classes } = this;
      if (!this.showError || this.valid) return classes;
      return `invalid ${classes}`;
    },
  },

  methods: {
    onChange(isComplete) {
      if (isComplete) {
        createToken().then((result) => {
          if (!result.error) {
            const { token: { id: token } } = result;
            const email = this.getStoreValue({
              storeModule: this.emailStoreModule,
              key: 'stripeEmail',
            });

            this.createCustomerOnServer({ token, email })
              .then(({ data: { customer_id: customerId } }) => {
                this.updateStoreValue({
                  storeModule: this.customerIdStoreModule,
                  key: 'customerId',
                  value: customerId,
                });

                this.$emit('markErrorValidity', { key: 'card', isValid: true });
              }).catch((err) => {
                // set error message from object
                this.$emit('markErrorValidity', { key: 'card', isValid: false });
              });
          } else {
            console.log(result);
          }
        });
      } else {
        // "incomplete card information"
        this.$emit('markErrorValidity', { key: 'card', isValid: false });
      }
    },
  },
};
</script>
