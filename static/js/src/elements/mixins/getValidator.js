export default {
  methods: {
    getValidator({ storeModule, key }) {
      const getter = this.$store.getters[`${storeModule}/validatorByKey`];
      return getter(key);
    },
  },
};
