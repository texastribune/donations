import validate from 'validate.js';

export default {
  data() {
    return {
      errors: {
        card: {
          message: 'Please enter valid payment card information.',
          valid: false,
        },
      },
      showCardErrors: false,
      showNativeErrors: false,
    };
  },

  computed: {
    errorMessageCard() {
      let message = '';

      Object.keys(this.errors).forEach((key) => {
        const curr = this.errors[key];
        if (!curr.valid) message += ` ${curr.message}`;
      });

      return message;
    },

    errorMessageNative() {
      let message = '';

      Object.keys(this.errors).forEach((key) => {
        const curr = this.errors[key];
        if (!curr.valid && key !== 'card') {
          message += ` ${curr.message}`;
        }
      });

      return message;
    },

    showErrors() {
      return (
        (this.showCardErrors && this.errorMessageCard) ||
        (this.showNativeErrors && this.errorMessageNative)
      );
    },
  },

  methods: {
    onSubmit() {
      this.$refs.form.submit();
    },

    setValue({ key, value }) {
      this[key] = value;
    },

    markErrorValidity({ key, isValid }) {
      this.errors[key].valid = isValid;
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
