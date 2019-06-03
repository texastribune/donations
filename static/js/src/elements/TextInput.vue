<template>
  <div :class="classesWithValidation">
    <label v-if="hasLabel" :for="connector">{{ labelText }}</label>
    <input
      :id="connector"
      :aria-label="ariaLabel"
      :aria-invalid="!isValid ? true : false"
      :aria-required="required"
      :value="value"
      :name="name"
      :placeholder="placeholder"
      :type="type"
      :inputmode="inputmode"
      @input="updateSingleValue($event.target.value)"
    />
    <p v-if="showError && !isValid" role="alert">{{ message }}</p>
  </div>
</template>

<script>
import connectedElement from './mixins/connectedElement';
import labelConnector from './mixins/labelConnector';

export default {
  name: 'TextInput',

  mixins: [connectedElement, labelConnector],

  props: {
    hasLabel: {
      type: Boolean,
      default: true,
    },

    labelText: {
      type: String,
      required: true,
    },

    placeholder: {
      type: String,
      default: '',
    },

    required: {
      type: Boolean,
      default: true,
    },

    type: {
      type: String,
      default: 'text',
    },

    inputmode: {
      type: String,
      default: null,
      required: false,
    },
  },

  computed: {
    connector() {
      if (!this.hasLabel) return false;
      return `_${this.randConnector}`;
    },

    ariaLabel() {
      if (this.hasLabel) return false;
      return this.labelText;
    },

    classesWithValidation() {
      const { classes } = this;
      if (!this.showError || this.isValid) return classes;
      return `invalid ${classes}`;
    },
  },
};
</script>
