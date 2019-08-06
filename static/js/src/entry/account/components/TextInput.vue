<template>
  <div>
    <label v-if="showLabel" :for="name">{{ label }}</label>
    <input
      :id="name"
      :name="name"
      :value="value"
      :aria-label="showLabel ? false : label"
      :readonly="readOnly"
      type="text"
      @input="onInput"
      @paste="onPaste"
    />
    <ul v-show="showErrorMessages">
      <li v-for="message in errorMessages" :key="message">{{ message }}</li>
    </ul>
    <slot></slot>
  </div>
</template>

<script>
import formElementMixin from '../mixins/form-element';

export default {
  name: 'TextInput',

  mixins: [formElementMixin],

  props: {
    value: {
      type: String,
      required: true,
    },

    errorMessages: {
      type: Array,
      required: true,
    },

    preventPaste: {
      type: Boolean,
      default: false,
    },

    readOnly: {
      type: Boolean,
      default: false,
    },

    showLabel: {
      type: Boolean,
      default: true,
    },

    showErrorImmediately: {
      type: Boolean,
      default: true,
    },
  },

  computed: {
    showErrorMessages() {
      const { errorMessages, dirty, showErrorImmediately } = this;

      return (
        (errorMessages.length && !showErrorImmediately && dirty) ||
        (errorMessages.length && showErrorImmediately)
      );
    },
  },

  methods: {
    onInput(e) {
      this.$emit('input', e.target.value);
    },

    onPaste(e) {
      if (this.preventPaste) e.preventDefault();
    },
  },
};
</script>
