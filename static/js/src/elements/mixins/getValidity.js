export default {
  methods: {
    getValidity({ storeModule, key }) {
      const getter = this.$store.getters[`${storeModule}/validityByKey`];
      return getter(key);
    },
  },
};
