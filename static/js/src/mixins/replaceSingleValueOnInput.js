export default {
  props: {
    updateCallback: {
      type: Function,
      default: null,
    },
  },

  methods: {
    onInput(newValue) {
      this.$store.dispatch(
        `${this.storeModule}/updateValue`,
        { key: this.name, value: newValue },
      );

      if (this.updateCallback) this.updateCallback(newValue);
    },
  },
};
