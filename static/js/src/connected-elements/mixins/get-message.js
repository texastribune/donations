export default {
  methods: {
    getMessage({ storeModule, key }) {
      const getter = this.$store.getters[`${storeModule}/messageByKey`];
      return getter(key);
    },
  },
};
