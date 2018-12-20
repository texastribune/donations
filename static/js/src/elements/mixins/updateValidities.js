export default {
  methods: {
    updateValidities({ updates, storeModule }) {
      this.$store.dispatch(`${storeModule}/updateValidities`, updates);
    },
  },
};
