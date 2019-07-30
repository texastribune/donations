import { ValidationProvider } from 'vee-validate';

import TextInput from '../components/TextInput.vue';
import Submit from '../components/Submit.vue';

export default {
  components: { TextInput, Submit, ValidationProvider },

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
        key => this.currentFields[key].changed
      );

      return haveChanged.length > 0;
    },

    formIsValid() {
      const fieldsToValidate = Object.keys(this.currentFields).filter(key => {
        const { shouldValidate, isVisible } = this.currentFields[key];
        return shouldValidate && isVisible;
      });

      const areNotValid = fieldsToValidate.filter(
        key => !this.currentFields[key].valid
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
      const updateKeys = ['isVisible', 'shouldValidate', 'value'];

      Object.keys(this.initialFields).forEach(fieldKey => {
        updateKeys.forEach(updateKey => {
          this.$set(
            this.currentFields[fieldKey],
            updateKey,
            this.initialFields[fieldKey][updateKey]
          );
        });
      });
    },

    buildCurrentFields() {
      const final = {};

      Object.keys(this.initialFields).forEach(key => {
        const { value, shouldValidate, isVisible } = this.initialFields[key];

        final[key] = {
          value,
          isVisible,
          shouldValidate,
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
