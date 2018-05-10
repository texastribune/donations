export default {
  methods: {
    onInput(newValue) {
      this.$store.dispatch(
        `${this.storeModule}/updateValue`,
        { key: this.name, value: newValue },
      );

      this.$emit('updateCallback', newValue);
      if (this.validator) this.validate(newValue);
    },
  },
};
