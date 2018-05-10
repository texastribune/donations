export default {
  props: {
    updateCallback: {
      type: Function,
      required: true,
    },
  },

  methods: {
    onInput(newValue) {
      this.updateCallback(newValue);
    },
  },
};
