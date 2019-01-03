export default {
  data() {
    return {
      card: {
        isValid: false,
        message: 'Your card number is incomplete',
      },
      stripeToken: '',
      showErrors: false,
      showCardError: false,
      showManualPay: false,
      nativeIsSupported: false,
      isFetchingToken: false,
    };
  },

  computed: {
    isValid() {
      const fields = this.$store.state[this.storeModule];
      const invalids = Object.keys(fields).filter(key => !fields[key].isValid);

      return invalids.length === 0;
    },

    showErrorClue() {
      if (this.showCardError && !this.card.isValid) return true;
      if (this.showErrors && !this.isValid) return true;

      return false;
    },

    showServerErrorMessage() {
      return !this.showErrorClue && this.serverErrorMessage;
    },
  },

  methods: {
    onSubmit() {
      this.$refs.form.submit();
    },

    setLocalValue(updates) {
      if (Array.isArray(updates)) {
        updates.forEach(({ key, value }) => {
          this[key] = value;
        });
      } else {
        const { key, value } = updates;
        this[key] = value;
      }
    },

    setCardValue(updates) {
      if (Array.isArray(updates)) {
        updates.forEach(({ key, value }) => {
          this.card[key] = value;
        });
      } else {
        const { key, value } = updates;
        this.card[key] = value;
      }
    },
  },
};
