export default {
  methods: {
    getStoreValue({ storeModule, key }) {
      const getter = this.$store.getters[`${storeModule}/valueByKey`];
      return getter(key);
    },
  },
};
