<template>
  <div>
    <label :for="name">{{ label }}</label>
    <input
      :id="name"
      :key="name"
      :name="name"
      :value="value"
      type="text"
      @input="onInput"
      @paste="onPaste"
    />
    <ul v-if="errorMessages.length">
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
  },

  computed: {
    changed() {
      return this.flags.changed;
    },

    valid() {
      return this.flags.valid;
    },
  },

  watch: {
    changed() {
      this.addFlags();
    },

    valid() {
      this.addFlags();
    },
  },

  methods: {
    onInput(e) {
      this.$emit('input', e.target.value);
    },

    onPaste(e) {
      if (this.preventPaste) {
        e.preventDefault();
      }
    },

    addFlags() {
      const { changed, valid } = this;
      this.$emit('addFlags', this.name, { changed, valid });
    },
  },
};
</script>
