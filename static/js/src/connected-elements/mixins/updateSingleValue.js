export default {
  methods: {
    updateSingleValue(newValue) {
      this.$store.dispatch(
        `${this.storeModule}/updateValue`,
        { key: this.name, value: newValue },
      );

      this.$emit('updateCallback', newValue);
    },
  },
};
