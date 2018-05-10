import validate from 'validate.js';

export default {
  methods: {
    isValidEmail(email) {
      const isValid = validate(
        { from: email },
        { from: { email: true } },
      );
      return typeof isValid === 'undefined';
    },
  },
};
