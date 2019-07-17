export default {
  methods: {
    updateValues({ storeModule, updates }) {
      this.$store.dispatch(`${storeModule}/updateValues`, updates);
    },
  },
};
