<template>
  <input
    :class="classes"
    :value="value"
    :disabled="isFetchingToken"
    type="submit"
    @click="onClick"
  />
</template>

<script>
import Vue from 'vue';
import { createToken } from 'vue-stripe-elements-plus';

export default {
  name: 'ManualSubmit',

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
      this.$emit('setLocalValue', { key: 'isFetchingToken', value: true });
    },

    markNotFetchingToken() {
      this.$emit('setLocalValue', { key: 'isFetchingToken', value: false });
    },

    onClick() {
      const updates = [
        { key: 'showErrors', value: true },
        { key: 'showCardError', value: true },
        { key: 'serverErrorMessage', value: '' },
      ];

      this.$emit('setLocalValue', updates);

      if (this.formIsValid) {
        this.markFetchingToken();

        createToken().then(result => {
          if (!result.error) {
            const {
              token: { id },
            } = result;

            this.$emit('setLocalValue', {
              key: 'stripeToken',
              value: id,
            });

            Vue.nextTick(() => {
              this.$emit('onSubmit');
            });
          } else {
            const {
              error: { message, type },
            } = result;
            let messageToShow;

            this.markNotFetchingToken();

            if (type === 'validation_error') {
              messageToShow = message;
            } else {
              messageToShow = this.blanketErrorMessage;
            }

            this.$emit('setCardValue', [
              { key: 'isValid', value: false },
              { key: 'message', value: messageToShow },
            ]);
          }
        });
      }
    },
  },
};
</script>
