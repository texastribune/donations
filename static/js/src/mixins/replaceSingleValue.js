export default {
  methods: {
    replaceSingleValue({ newValue, storeModule, name }) {
      this.$store.dispatch(
        `${storeModule}/updateValue`,
        { key: name, value: newValue },
      );
    },
  },
};
