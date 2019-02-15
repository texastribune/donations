export default {
  methods: {
    updateValue({ storeModule, key, value }) {
      this.$store.dispatch(`${storeModule}/updateValue`, { key, value });
    },
  },
};
