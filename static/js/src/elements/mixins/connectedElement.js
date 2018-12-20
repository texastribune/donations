import getValue from './getValue';
import getValidator from './getValidator';
import getValidity from './getValidity';
import getMessage from './getMessage';
import updateValue from './updateValue';
import updateValidity from './updateValidity';
import * as validatorFns from '../../utils/validators';

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
      if (!this.validator) return true;

      return this.getValidity({
        storeModule: this.storeModule,
        key: this.name,
      });
    },

    validator() {
      const validator = this.getValidator({
        storeModule: this.storeModule,
        key: this.name,
      });

      if (!validator) return false;
      return validatorFns[validator];
    },

    message() {
      return this.message({
        storeModule: this.storeModule,
        key: this.name,
      });
    },
  },

  mounted() {
    if (!this.validator) return;
    if (this.validator(this.value)) this.markValid();
  },

  methods: {
    updateSingleValue(newValue) {
      if (!this.validator) {
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
