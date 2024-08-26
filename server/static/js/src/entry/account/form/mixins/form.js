import { ValidationProvider, ValidationObserver } from 'vee-validate';

import TextInput from '../components/TextInput.vue';
import Checkbox from '../components/Checkbox.vue';
import Radios from '../components/Radios.vue';
import Submit from '../components/Submit.vue';

export default {
  components: {
    TextInput,
    Checkbox,
    Submit,
    Radios,
    ValidationProvider,
    ValidationObserver,
  },

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
    onSubmit() {
      this.$emit('onSubmit', this.currentFields);
    },

    updateCurrentFields() {
      this.$set(this, 'currentFields', this.buildCurrentFields());
    },

    buildCurrentFields() {
      const final = {};

      Object.keys(this.initialFields).forEach(fieldName => {
        const value = this.initialFields[fieldName];

        final[fieldName] = {
          value,
          pristine: true,
          changed: false,
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

    emptyOutField(fieldName) {
      this.currentFields[fieldName].value = '';
    },
  },
};
