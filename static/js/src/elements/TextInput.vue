<template>
  <div
    :class="classes"
  >
    <label
      v-if="hasLabel"
      :for="connector"
      :class="getClasses({ elName: 'label' })"
    >
      {{ labelText }}
    </label>
    <input
      :id="connector"
      :aria-label="ariaLabel"
      :value="value"
      :name="name"
      :placeholder="placeholder"
      :class="inputClassesWithValidation"
      :type="type"
      @input="updateSingleValue($event.target.value)"
    >
    <p
      v-if="showError && !valid"
      :class="getClasses({ elName: 'error' })"
    >
      {{ errorMessage }}
    </p>
  </div>
</template>

<script>
import connectedElement from './mixins/connectedElement';

export default {
  name: 'TextInput',

  mixins: [connectedElement],

  props: {
    errorClasses: {
      type: String,
      default: '',
    },

    hasLabel: {
      type: Boolean,
      default: false,
    },

    labelClasses: {
      type: String,
      default: '',
    },

    labelText: {
      type: String,
      default: '',
    },

    maxlength: {
      type: [String, Boolean],
      default: false,
    },

    placeholder: {
      type: String,
      default: '',
    },

    type: {
      type: String,
      default: 'text',
    },
  },

  computed: {
    connector() {
      if (!this.hasLabel) return false;
      return this.name;
    },

    ariaLabel() {
      if (this.hasLabel) return false;
      return this.name;
    },

    inputClassesWithValidation() {
      const classes = this.getClasses({ elName: 'input' });
      if (!this.showError || this.valid) return classes;
      return `invalid ${classes}`;
    },
  },
};
</script>
