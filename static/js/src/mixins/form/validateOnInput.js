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

  mounted() {
    if (this.validator) this.validate(this.value);
  },

  methods: {
    validate(value) {
      let message = '';

      if (!this.validator(value)) {
        message = this.errorMessage;
      }

      this.$emit('addError', this.name, message);
    },
  },
};
