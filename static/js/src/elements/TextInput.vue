<template>
  <div
    :class="classesWithValidation"
  >
    <label
      v-if="hasLabel"
      :for="connector"
    >
      {{ labelText }}
    </label>
    <input
      :id="connector"
      :aria-label="ariaLabel"
      :aria-invalid="!valid ? true : false"
      :aria-required="required"
      :value="value"
      :name="name"
      :placeholder="placeholder"
      :type="type"
      @change="updateSingleValue($event.target.value)"
    >
    <p
      v-if="showError && !valid"
      role="alert"
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
    hasLabel: {
      type: Boolean,
      default: false,
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

    required: {
      type: Boolean,
      default: true,
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

    classesWithValidation() {
      const { classes } = this;
      if (!this.showError || this.valid) return classes;
      return `invalid ${classes}`;
    },
  },
};
</script>
