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

    formIsValid() {
      const fieldsToValidate = Object.keys(this.currentFields).filter(
        fieldName => {
          const { isVisible } = this.currentFields[fieldName];
          return isVisible;
        }
      );

      const areNotValid = fieldsToValidate.filter(
        fieldName => !this.currentFields[fieldName].valid
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
          changed: null,
          dirty: null,
          valid: null,
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
