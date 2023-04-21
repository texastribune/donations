export default {
  methods: {
    getValue({ storeModule, key }) {
      const getter = this.$store.getters[`${storeModule}/valueByKey`];
      return getter(key);
    },
  },
};
