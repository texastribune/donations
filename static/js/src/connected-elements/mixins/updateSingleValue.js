export default {
  props: {
    validator: {
      type: Function,
      default: null,
    },
  },

  mounted() {
    this.updateSingleValue(this.value);
  },

  methods: {
    updateSingleValue(newValue) {
      if (this.validator && this.validator(newValue)) {
        this.fireDispatch(newValue);
        this.fireUpdateCallback();
        this.markValid();
      } else if (this.validator && !this.validator(newValue)) {
        this.markInvalid();
      } else {
        this.fireDispatch(newValue);
        this.fireUpdateCallback();
      }
    },

    fireDispatch(value) {
      this.$store.dispatch(
        `${this.storeModule}/updateValue`,
        { key: this.name, value },
      );
    },

    fireUpdateCallback() {
      this.$emit('updateCallback', this.value);
    },

    markValid() {
      this.$emit('markValidity', this.name, true);
    },

    markInvalid() {
      this.$emit('markValidity', this.name, false);
    },
  },
};
