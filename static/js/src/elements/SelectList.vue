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

  <select
    :aria-labelledby="ariaLabelledby"
    :aria-describedby="ariaDescribedby"
    :aria-label="ariaLabel"
    :aria-invalid="!valid ? true : false"
    :aria-required="required"
    :class="classes">
    <option
      v-for="(option, index) in options.list"
        :selected="index == options.default"
        :id="getConnector(index)"
        :key="option.value"
        :value="option.value" >
        {{ option.text }}
    </option>
  </select>
  </div>
</template>

<script>
import connectedElement from './mixins/connectedElement';
import labelConnector from './mixins/labelConnector';
import aria from './mixins/aria';

export default {
  name: 'SelectList',

  mixins: [
    aria,
    connectedElement,
    labelConnector,
  ],

  props: {
    options: {
      type: Object,
      required: true,
    },

    hasLabel: {
      type: Boolean,
      default: true,
    },

    labelText: {
      type: String,
      required: true,
    },

   required: {
      type: Boolean,
      default: true,
    },

    type: {
      type: String,
      default: 'select',
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
      if (!this.showError || this.valid) return classes;
      return `invalid ${classes}`;
    },
  },

    methods: {
    getConnector(index) {
      return `_${this.randConnector}-${index}`;
    },
  },

};
</script>
