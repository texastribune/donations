import validate from 'validate.js';

export default {
  data() {
    return {
      validation: {
        card: {
          manual: true,
          native: false,
          valid: false,
          message: 'Your card number is incomplete',
        },
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
      const manualErrors =
        Object.keys(this.validation).filter((key) => {
          const curr = this.validation[key];
          return !curr.valid && curr.manual;
        });
      return manualErrors.length === 0;
    },

    nativeIsValid() {
      const nativeErrors =
        Object.keys(this.validation).filter((key) => {
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

    setValidationValue(updates) {
      if (Array.isArray(updates)) {
        updates.forEach(({ element, key, value }) => {
          this.validation[element][key] = value;
        });
      } else {
        const { element, key, value } = updates;
        this.validation[element][key] = value;
      }
    },

    isEmail(value) {
      const isValid = validate(
        { email: value.trim() },
        { email: { email: true } },
      );
      return typeof isValid === 'undefined';
    },

    isNumeric(value) {
      const isValid = validate(
        { value: value.trim() },
        { value: { numericality: true } },
      );
      return typeof isValid === 'undefined';
    },

    isZip(value) {
      return this.isNumeric(value) && value.trim().length === 5;
    },

    isNotEmpty(value) {
      return !validate.isEmpty(value.trim());
    },

    isEmptyOrZip(value) {
      if (!this.isNotEmpty(value)) return true;
      return this.isZip(value);
    },

    isValidDonationAmount(value) {
      const isValid = validate(
        { value: value.trim() },
        { value: { numericality: { greaterThanOrEqualTo: 1 } } },
      );
      return typeof isValid === 'undefined';
    },

    isValidReason(value) {
      return value.trim().length <= 255;
    },
  },
};
