<template>
  <div :class="classesWithValidation">
    <div ref="manual" />
    <p v-if="showError && !isValid" role="alert">{{ message }}</p>
  </div>
</template>

<script>
/* global Stripe */

export default {
  name: 'ManualPay',

  props: {
    showError: {
      type: Boolean,
      default: false,
    },

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
      // eslint-disable-next-line no-underscore-dangle
      return window.__STRIPE_KEY__;
    },

    isValid() {
      return this.card.isValid;
    },

    message() {
      return this.card.message;
    },

    classesWithValidation() {
      const { classes } = this;
      if (!this.showError || this.isValid) return classes;
      return `invalid ${classes}`;
    },
  },

  mounted() {
    const stripe = new Stripe(this.stripeKey);
    window.stripe = stripe;

    const elements = stripe.elements();
    const card = elements.create('card');
    window.stripeCard = card;

    card.mount(this.$refs.manual, this.options);
    card.addEventListener('change', event => {
      this.onChange(event);
    });
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
        { key: 'message', value: messageValue },
      ]);
    },
  },
};
</script>
