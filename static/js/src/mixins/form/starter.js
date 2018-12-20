export default {
  data() {
    return {
      card: {
        isValid: false,
        message: 'Your card number is incomplete',
      },
      stripeToken: '',
      showManualErrors: false,
      showNativeErrors: false,
      showManualPay: false,
      nativeIsSupported: false,
      isFetchingToken: false,
    };
  },

  computed: {
    manualIsValid() {
      const manualErrors = Object.keys(this.validation).filter(key => {
        const curr = this.validation[key];
        return !curr.valid && curr.manual;
      });
      return manualErrors.length === 0;
    },

    nativeIsValid() {
      const nativeErrors = Object.keys(this.validation).filter(key => {
        const curr = this.validation[key];
        return !curr.valid && curr.native;
      });
      return nativeErrors.length === 0;
    },

    showErrorClue() {
      if (this.showManualErrors && !this.manualIsValid) return true;
      if (this.showNativeErrors && !this.nativeIsValid) return true;
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

    setValue(updates) {
      if (Array.isArray(updates)) {
        updates.forEach(({ key, value }) => {
          this[key] = value;
        });
      } else {
        const { key, value } = updates;
        this[key] = value;
      }
    },
  },
};
