import validate from 'validate.js';

export default {
  data() {
    return {
      validation: {
        card: {
          manual: true,
          native: false,
          valid: false,
          message: 'Invalid card information',
        },
      },
      showManualErrors: false,
      showNativeErrors: false,
      showManualPay: false,
      nativeIsSupported: false,
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
  },

  methods: {
    onSubmit() {
      this.$refs.form.submit();
    },

    markErrorValidity({ key, isValid }) {
      this.validation[key].valid = isValid;
    },

    setValue({ key, value }) {
      this[key] = value;
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
  },
};
