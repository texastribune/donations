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
    onInput(newValue) {
      this.$store.dispatch(
        `${this.storeModule}/updateValue`,
        { key: this.name, value: newValue },
      );

      this.$emit('updateCallback', newValue);
      if (this.validator) this.validate(newValue);
    },

    validate(value) {
      let message = '';

      if (!this.validator(value)) {
        message = this.errorMessage;
      }

      this.$emit('addError', this.name, message);
    },
  },
};
