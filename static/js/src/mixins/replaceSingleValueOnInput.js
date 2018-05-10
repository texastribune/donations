export default {
  props: {
    updateCallback: {
      type: Function,
      default: null,
    },

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
    this.validate(this.value);
  },

  methods: {
    onInput(newValue) {
      this.$store.dispatch(
        `${this.storeModule}/updateValue`,
        { key: this.name, value: newValue },
      );

      if (this.updateCallback) this.updateCallback(newValue);

      this.validate(newValue);
    },

    validate(value) {
      if (this.validator) {
        if (!this.validator(value)) {
          this.$emit('addError', this.name, this.errorMessage);
        } else {
          this.$emit('addError', this.name, '');
        }
      }
    },
  },
};
