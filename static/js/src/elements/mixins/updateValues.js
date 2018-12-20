export default {
  methods: {
    updateValues({ updates, storeModule }) {
      this.$store.dispatch(`${storeModule}/updateValues`, updates);
    },
  },
};
