import validate from 'validate.js';

export default {
  methods: {
    isEmail(value) {
      const isValid = validate(
        { email: value.trim() },
        { email: { email: true } },
      );
      return typeof isValid === 'undefined';
    },

    isZip(value) {
      return this.isNumeric(value) && value.trim().length === 5;
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

    isNotEmpty(value) {
      return !validate.isEmpty(value.trim());
    },
  },
};
