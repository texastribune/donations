import getValue from './get-value';
import getValidator from './get-validator';
import getValidity from './get-validity';
import getMessage from './get-message';
import updateValue from './update-value';
import updateValidity from './update-validity';

export default {
  mixins: [
    getValue,
    getValidator,
    getValidity,
    getMessage,
    updateValue,
    updateValidity,
  ],

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
  },

  computed: {
    value() {
      return this.getValue({
        storeModule: this.storeModule,
        key: this.name,
      });
    },

    isValid() {
      return this.getValidity({
        storeModule: this.storeModule,
        key: this.name,
      });
    },

    validator() {
      return this.getValidator({
        storeModule: this.storeModule,
        key: this.name,
      });
    },

    message() {
      return this.getMessage({
        storeModule: this.storeModule,
        key: this.name,
      });
    },
  },

  mounted() {
    if (this.validator === null) return;
    if (this.validator(this.value)) this.markValid();
  },

  methods: {
    updateSingleValue(newValue) {
      if (this.validator === null) {
        this.fireDispatch(newValue);
        this.fireUpdateCallback(newValue);
      } else {
        if (this.validator(newValue)) {
          this.markValid();
          this.fireUpdateCallback(newValue);
        } else {
          this.markInvalid();
        }
        this.fireDispatch(newValue);
      }
    },

    fireUpdateCallback(value) {
      this.$emit('updateCallback', value);
    },

    markValid() {
      this.updateValidity({
        storeModule: this.storeModule,
        key: this.name,
        isValid: true,
      });
    },

    markInvalid() {
      this.updateValidity({
        storeModule: this.storeModule,
        key: this.name,
        isValid: false,
      });
    },

    fireDispatch(value) {
      this.updateValue({
        storeModule: this.storeModule,
        key: this.name,
        value,
      });
    },
  },
};
