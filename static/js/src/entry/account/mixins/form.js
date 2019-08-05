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
      keysInField: [],
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
          const { shouldValidate, isVisible } = this.currentFields[fieldName];
          return shouldValidate && isVisible;
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
      Object.keys(this.initialFields).forEach(fieldName => {
        this.keysInField.forEach(keyInField => {
          this.currentFields[fieldName][keyInField] = this.initialFields[
            fieldName
          ][keyInField];
        });
      });
    },

    buildCurrentFields() {
      const final = {};

      Object.keys(this.initialFields).forEach((fieldName, index) => {
        const { value, shouldValidate, isVisible, rules } = this.initialFields[
          fieldName
        ];

        final[fieldName] = {
          value,
          rules,
          isVisible,
          shouldValidate,
          changed: null,
          dirty: null,
          valid: null,
        };

        if (index === 0) {
          this.keysInField = [...Object.keys(final[fieldName])];
        }
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
