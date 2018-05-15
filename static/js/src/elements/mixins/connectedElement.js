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

    validator: {
      type: Function,
      default: null,
    },
  },

  computed: {
    value() {
      const getter =
        this.$store.getters[`${this.storeModule}/valueByKey`];
      return getter(this.name);
    },
  },

  mounted() {
    if (this.validator && this.validator(this.value)) {
      this.markValid();
    }
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
      this.$emit('markErrorValidity', { key: this.name, isValid: true });
    },

    markInvalid() {
      this.$emit('markErrorValidity', { key: this.name, isValid: false });
    },
  },
};
