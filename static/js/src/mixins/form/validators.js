import validate from 'validate.js';

export default {
  methods: {
    isEmail(value) {
      const isValid = validate(
        { from: value.trim() },
        { from: { email: true } },
      );
      return typeof isValid === 'undefined';
    },

    isZip(value) {
      return this.isNumeric(value) && value.trim().length === 5;
    },

    isNumeric(value) {
      return validate.isNumber(parseFloat(value.trim()));
    },

    isNotEmpty(value) {
      return !validate.isEmpty(value.trim());
    },

    isEmptyOrZip(value) {
      if (!this.isNotEmpty(value)) return true;
      return this.isZip(value);
    },
  },
};
