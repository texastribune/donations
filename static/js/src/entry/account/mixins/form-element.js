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

    dirty() {
      return this.flags.dirty;
    },
  },

  watch: {
    changed() {
      this.updateFlags();
    },

    valid() {
      this.updateFlags();
    },

    dirty() {
      this.updateFlags();
    },
  },

  methods: {
    updateFlags() {
      const { changed, valid, dirty } = this;
      this.$emit('updateFlags', this.name, { changed, valid, dirty });
    },
  },
};
