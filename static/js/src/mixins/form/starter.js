export default {
  data() {
    return {
      // card input is the only input not stored
      // at the Vuex level
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
    // Returns true if all form values at the Vuex level are valid.
    // This does NOT account for local `card` validity
    isValid() {
      const fields = this.$store.state[this.storeModule];
      const invalids = Object.keys(fields).filter(key => !fields[key].isValid);

      return invalids.length === 0;
    },

    // whether to show "please correct errors above" below form
    showErrorClue() {
      if (this.showCardError && !this.card.isValid) return true;
      if (this.showErrors && !this.isValid) return true;

      return false;
    },

    // whether to show card-failure message produced on the server
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
