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

    flags: {
      type: Object,
      required: true,
    },
  },

  computed: {
    changed() {
      return this.flags.changed;
    },

    valid() {
      return this.flags.valid;
    },

    pristine() {
      return this.flags.pristine;
    },
  },

  watch: {
    changed() {
      this.updateFlags();
    },

    valid() {
      this.updateFlags();
    },

    pristine() {
      this.updateFlags();
    },
  },

  methods: {
    updateFlags() {
      const { changed, valid, pristine } = this;
      this.$emit('updateFlags', this.name, { changed, valid, pristine });
    },
  },
};
