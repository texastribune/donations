export default {
  props: {
    name: {
      type: String,
      required: true,
    },

    showError: {
      type: Boolean,
      default: false,
    },

    storeModule: {
      type: String,
      required: true,
    },

    validation: {
      type: Object,
      default: null,
    },
  },

  computed: {
    value() {
      const getter =
        this.$store.getters[`${this.storeModule}/valueByKey`];
      return getter(this.name);
    },

    valid() {
      if (!this.validation) return true;
      return this.validation.valid;
    },

    errorMessage() {
      if (!this.validation) return '';
      return this.validation.message;
    },
  },

  mounted() {
    if (!this.validation) return;
    if (this.validation.validator(this.value)) this.markValid();
  },

  methods: {
    updateSingleValue(newValue) {
      if (!this.validation) {
        this.fireDispatch(newValue);
        this.fireUpdateCallback(newValue);
      } else {
        if (this.validation.validator(newValue)) {
          this.markValid();
          this.fireUpdateCallback(newValue);
        } else {
          this.markInvalid();
        }

        this.fireDispatch(newValue);
      }
    },

    fireDispatch(value) {
      this.$store.dispatch(
        `${this.storeModule}/updateValue`,
        { key: this.name, value },
      );
    },

    fireUpdateCallback(value) {
      this.$emit('updateCallback', value);
    },

    markValid() {
      this.$emit('setValidationValue', { element: this.name, key: 'valid', value: true });
    },

    markInvalid() {
      this.$emit('setValidationValue', { element: this.name, key: 'valid', value: false });
    },
  },
};
