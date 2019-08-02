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
export default {
  name: 'TextInput',

  props: {
    value: {
      type: String,
      required: true,
    },

    name: {
      type: String,
      required: true,
    },

    label: {
      type: String,
      required: true,
    },

    flags: {
      type: Object,
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
    changed() {
      return this.flags.changed;
    },

    valid() {
      return this.flags.valid;
    },

    dirty() {
      return this.flags.dirty;
    },

    showErrorMessages() {
      const { errorMessages, dirty, showErrorImmediately } = this;

      return (
        (errorMessages.length && !showErrorImmediately && dirty) ||
        (errorMessages.length && showErrorImmediately)
      );
    },
  },

  watch: {
    changed() {
      this.updateFlags();
    },

    valid() {
      this.updateFlags();
    },

    dirty() {
      this.updateFlags();
    },
  },

  methods: {
    onInput(e) {
      this.$emit('input', e.target.value);
    },

    onPaste(e) {
      if (this.preventPaste) e.preventDefault();
    },

    updateFlags() {
      const { changed, valid, dirty } = this;
      this.$emit('updateFlags', this.name, { changed, valid, dirty });
    },
  },
};
</script>
