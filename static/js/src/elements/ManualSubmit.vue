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

import updateValidity from './mixins/updateValidity';

export default {
  name: 'ManualSubmit',

  mixins: [updateValidity],

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
        { key: 'serverErrorMessage', value: '' },
      ];

      this.$emit('setValue', updates);

      if (this.formIsValid) {
        this.markFetchingToken();

        createToken().then((result) => {
          if (!result.error) {
            const { token: { id } } = result;

            this.$emit('setValue', {
              key: 'stripeToken',
              value: id,
            });

            Vue.nextTick(() => { this.$emit('onSubmit'); });
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
