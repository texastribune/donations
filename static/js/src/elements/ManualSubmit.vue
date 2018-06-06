<template>
  <input
    :class="classes"
    :value="value"
    :disabled="isFetchingToken"
    type="submit"
    @click="onClick"
  >
</template>

<script>
import Vue from 'vue';
import { createToken } from 'vue-stripe-elements-plus';

import updateStoreValue from './mixins/updateStoreValue';
import getStoreValue from './mixins/getStoreValue';
import updateValidity from './mixins/updateValidity';
import createCustomer from '../utils/createCustomer';

export default {
  name: 'ManualSubmit',

  mixins: [
    updateStoreValue,
    updateValidity,
    getStoreValue,
  ],

  props: {
    value: {
      type: String,
      default: 'Submit',
    },

    formIsValid: {
      type: Boolean,
      required: true,
    },

    isFetchingToken: {
      type: Boolean,
      required: true,
    },

    customerIdStoreModule: {
      type: String,
      required: true,
    },

    emailStoreModule: {
      type: String,
      required: true,
    },
  },

  data() {
    return {
      blanketErrorMessage: `
        There was an issue processing your card.
        Please try a different card and submit
        the form again. If the issue persists, contact
        inquiries@texastribune.org.
      `,
    };
  },

  methods: {
    isUnexpectedError({ status, expected }) {
      if (status !== 400 || !expected) return true;
      return false;
    },

    markFetchingToken() {
      this.$emit('setValue', { key: 'isFetchingToken', value: true });
    },

    markNotFetchingToken() {
      this.$emit('setValue', { key: 'isFetchingToken', value: false });
    },

    onClick() {
      const updates = [
        { key: 'showManualErrors', value: true },
        { key: 'showNativeErrors', value: false },
      ];

      this.$emit('setValue', updates);

      if (this.formIsValid) {
        this.markFetchingToken();

        createToken().then((result) => {
          if (!result.error) {
            const { token: { id: token } } = result;
            const email = this.getStoreValue({
              storeModule: this.emailStoreModule,
              key: 'stripeEmail',
            });

            /**
              Because Stripe 3 does not validate cards client side,
              we have to create the customer on the server and
              check for errors returned there. If they exist,
              we display them. If not, we store the returned customer ID.
            */
            createCustomer({ token, email })
              .then(({ data: { customer_id: customerId } }) => {
                this.updateStoreValue({
                  storeModule: this.customerIdStoreModule,
                  key: 'customerId',
                  value: customerId,
                });

                Vue.nextTick(() => { this.$emit('onSubmit'); });
              })
              .catch(({
                response: {
                  status,
                  data: { type, message, expected },
                },
              }) => {
                let element;
                let messageToShow;
                const isUnexpectedError =
                  this.isUnexpectedError({ status, expected });

                if (isUnexpectedError) {
                  messageToShow = this.blanketErrorMessage;
                  element = 'card';
                } else if (type === 'email') {
                  messageToShow = message;
                  element = 'stripeEmail';
                } else if (type === 'card') {
                  messageToShow = message;
                  element = 'card';
                }

                this.markMessageAndInvalid({ element, message: messageToShow });
                this.markNotFetchingToken();
              });
          } else {
            const { error: { message, type } } = result;
            let messageToShow;

            this.markNotFetchingToken();

            if (type === 'validation_error') {
              messageToShow = message;
            } else {
              messageToShow = this.blanketErrorMessage;
            }

            this.markMessageAndInvalid({
              element: 'card',
              message: messageToShow,
            });
          }
        });
      }
    },
  },
};
</script>
