export default {
  props: {
    validator: {
      type: Function,
      default: null,
    },

    errorMessage: {
      type: String,
      default: 'Invalid input',
    },
  },

  methods: {
    validate(value) {
      let message = '';

      if (!this.validator(value)) message = this.errorMessage;

      this.$emit('addError', this.name, message);
    },
  },
};
