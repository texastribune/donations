export default {
  methods: {
    markValid(element) {
      this.$emit('setValidationValue', { element, key: 'valid', value: true });
    },

    markInvalid(element) {
      this.$emit('setValidationValue', { element, key: 'valid', value: false });
    },

    markMessageAndInvalid({ element, message }) {
      const updates = [
        { element, key: 'valid', value: false },
        { element, key: 'message', value: message },
      ];

      this.$emit('setValidationValue', updates);
    },
  },
};
