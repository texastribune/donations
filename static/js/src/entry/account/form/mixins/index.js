import { ValidationProvider } from 'vee-validate';

import TextInput from '../components/TextInput.vue';
import Checkbox from '../components/Checkbox.vue';
import Submit from '../components/Submit.vue';

export default {
  components: { TextInput, Checkbox, Submit, ValidationProvider },

  props: {
    initialFields: {
      type: Object,
      required: true,
    },
  },

  data() {
    return {
      currentFields: this.buildCurrentFields(),
      formKey: Date.now().toString(),
    };
  },

  computed: {
    formHasChanged() {
      const haveChanged = Object.keys(this.currentFields).filter(
        fieldName => this.currentFields[fieldName].changed
      );

      return haveChanged.length > 0;
    },

    formIsPristine() {
      const areNotPristine = Object.keys(this.currentFields).filter(
        fieldName => !this.currentFields[fieldName].pristine
      );

      return areNotPristine.length === 0;
    },

    formIsValid() {
      const visibleFields = Object.keys(this.currentFields).filter(
        fieldName => this.currentFields[fieldName].isVisible
      );

      const areNotValid = visibleFields.filter(
        // explicitly check for false because value can also be null
        fieldName => this.currentFields[fieldName].valid === false
      );

      return areNotValid.length === 0;
    },
  },

  watch: {
    formHasChanged(newHasChanged, oldHasChanged) {
      if (newHasChanged !== oldHasChanged) {
        this.$emit('onFormHasChangedToggle', newHasChanged);
      }
    },

    formIsPristine(newIsPristine, oldIsPristine) {
      if (newIsPristine !== oldIsPristine) {
        this.$emit('onFormIsPristineToggle', newIsPristine);
      }
    },

    initialFields() {
      this.updateCurrentFields();
      this.formKey = Date.now().toString();
    },
  },

  methods: {
    updateCurrentFields() {
      this.$set(this, 'currentFields', this.buildCurrentFields());
    },

    buildCurrentFields() {
      const final = {};

      Object.keys(this.initialFields).forEach(fieldName => {
        const { ...allValues } = this.initialFields[fieldName];

        final[fieldName] = {
          ...allValues,
          pristine: true, // default vee-validate flag value
          changed: false, // default vee-validate flag value
          valid: null, // default vee-validate flag value
        };
      });

      return final;
    },

    updateFlags(fieldName, flags) {
      this.currentFields[fieldName] = {
        ...this.currentFields[fieldName],
        ...flags,
      };
    },

    resetValue(fieldName) {
      this.currentFields[fieldName].value = '';
    },
  },
};
