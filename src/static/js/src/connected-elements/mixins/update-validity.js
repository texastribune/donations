export default {
  methods: {
    updateValidity({ storeModule, key, isValid }) {
      this.$store.dispatch(`${storeModule}/updateValidity`, {
        key,
        isValid,
      });
    },
  },
};
