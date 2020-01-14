export default {
  props: {
    name: {
      type: String,
      required: true,
    },

    label: {
      type: String,
      required: true,
    },

    pristine: {
      type: Boolean,
      required: true,
    },

    changed: {
      type: Boolean,
      required: true,
    },

    valid: {
      type: Boolean,
      required: true,
    },
  },

  watch: {
    changed() {
      this.updateFlags();
    },

    pristine() {
      this.updateFlags();
    },

    valid() {
      this.updateFlags();
    },
  },

  methods: {
    updateFlags() {
      const { changed, pristine, valid } = this;

      this.$emit('updateFlags', this.name, { changed, pristine, valid });
    },
  },
};
