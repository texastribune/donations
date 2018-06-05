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

    markValid() {
      this.$emit('setValidationValue', { element: 'card', key: 'valid', value: true });
    },

    markErrorAndInvalid(message) {
      const updates = [
        { element: 'card', key: 'valid', value: false },
        { element: 'card', key: 'message', value: message },
      ];

      this.$emit('setValidationValue', updates);
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
                this.markValid();
                this.updateStoreValue({
                  storeModule: this.customerIdStoreModule,
                  key: 'customerId',
                  value: customerId,
                });
              }).catch(({ response: { data: { error: message } } }) => {
                this.markErrorAndInvalid(message);
              })
              .then(() => {
                this.markNotFetchingToken();
              });
          } else {
            this.markNotFetchingToken();
            this.markErrorAndInvalid(result.error.message);
          }
        });
      } else {
        const message = 'Incomplete card input';
        this.markErrorAndInvalid(message);
      }
    },
  },
};
</script>
