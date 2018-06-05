<template>
  <div
    :class="classesWithValidation"
  >
    <card
      ref="card"
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
import Vue from 'vue';

import updateStoreValue from './mixins/updateStoreValue';
import getStoreValue from './mixins/getStoreValue';
import createCustomer from '../utils/createCustomer';

export default {
  name: 'ManualPay',

  components: {
    Card,
  },

  mixins: [
    updateStoreValue,
    getStoreValue,
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
    markFetchingToken() {
      this.$emit('setValue', { key: 'isFetchingToken', value: true });
    },

    markNotFetchingToken() {
      this.$emit('setValue', { key: 'isFetchingToken', value: false });
    },

    markValid(element) {
      this.$emit('setValidationValue', { element, key: 'valid', value: true });
    },

    markInvalid(element) {
      this.$emit('setValidationValue', { element, key: 'valid', value: false });
    },

    markErrorAndInvalid({ element, message }) {
      const updates = [
        { element, key: 'valid', value: false },
        { element, key: 'message', value: message },
      ];

      this.$emit('setValidationValue', updates);
    },

    showManualErrors() {
      this.$emit('setValue', { key: 'showManualErrors', value: true });
    },

    onChange(isComplete) {
      if (isComplete) {
        this.markFetchingToken();

        createToken().then((result) => {
          if (!result.error) {
            const { token: { id: token } } = result;
            const email = this.getStoreValue({
              storeModule: this.emailStoreModule,
              key: 'stripeEmail',
            });

            /**
             Because Stripe 3 does not validate CVC client side,
             we have to create the customer on the server and
             check for errors returned there. If they exist,
             we display them. If not, we store the returned customer ID.
            */
            createCustomer({ token, email })
              .then(({ data: { customer_id: customerId } }) => {
                this.markValid('card');
                this.updateStoreValue({
                  storeModule: this.customerIdStoreModule,
                  key: 'customerId',
                  value: customerId,
                });
              }).catch(({ response: { data: { type, message } } }) => {
                let element;

                this.showManualErrors();

                if (type === 'email') {
                  this.$refs.card.clear();
                  element = 'stripeEmail';
                } else if (type === 'card') {
                  element = 'card';
                }

                this.markErrorAndInvalid({ element, message });
              })
              .then(() => {
                this.markNotFetchingToken();
              });
          } else {
            this.markNotFetchingToken();
            this.markErrorAndInvalid({
              element: 'card',
              message: result.error.message,
            });
          }
        });
      } else {
        this.markErrorAndInvalid({
          element: 'card',
          message: 'Incomplete card input',
        });
      }
    },
  },
};
</script>
