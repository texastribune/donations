export default {
  props: {
    identifier: {
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
      return getter(this.identifier);
    },
  },

  methods: {
    updateValue(newValue) {
      this.$store.dispatch(
        `${this.storeModule}/updateValue`,
        { key: this.identifier, value: newValue },
      );
    },
  },
};
