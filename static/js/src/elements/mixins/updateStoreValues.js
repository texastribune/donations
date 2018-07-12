export default {
  methods: {
    updateStoreValues({ updates, storeModule }) {
      this.$store.dispatch(
        `${storeModule}/updateValues`,
        updates,
      );
    },
  },
};
