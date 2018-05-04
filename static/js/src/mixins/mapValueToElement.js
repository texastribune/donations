export default {
  props: {
    name: {
      type: String,
      required: true,
    },

    storeModule: {
      type: String,
      required: true,
    },
  },

  computed: {
    value() {
      const getter = this.$store.getters[`${this.storeModule}/valueByKey`];
      return getter(this.name);
    },
  },
};
