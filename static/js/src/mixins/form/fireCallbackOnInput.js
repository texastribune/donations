export default {
  methods: {
    onInput(newValue) {
      this.$emit('updateCallback', newValue);
    },
  },
};
