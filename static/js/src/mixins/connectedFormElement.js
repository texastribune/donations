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
      const action = this.$store.actions[`${this.storeModule}/updateValue`];
      
      action({
        key: this.identifier,
        value: newValue,
      });
    },
  },
};
