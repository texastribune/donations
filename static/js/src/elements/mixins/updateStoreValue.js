export default {
  methods: {
    updateStoreValue({ storeModule, key, value }) {
      this.$store.dispatch(
        `${storeModule}/updateValue`,
        { key, value },
      );
    },
  },
};
