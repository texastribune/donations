<template>
  <div class="c-text-input">
    <label
      v-if="showLabel"
      :for="name"
      class="l-display-block has-xxxs-btm-marg t-size-s"
    >
      <strong>{{ label }}</strong>
    </label>
    <input
      :id="name"
      :name="name"
      :value="value"
      :aria-label="ariaLabel"
      :aria-invalid="hasErrors"
      :readonly="readOnly"
      :class="{
        'is-invalid': hasErrors,
        'has-xxxs-btm-marg': hasErrors || (!hasErrors && hasExtraSlot),
      }"
      class="c-text-input__input l-display-block l-width-full has-text-gray-dark t-lh-b"
      type="text"
      @input="onInput"
      @paste="onPaste"
    />
    <ul
      v-show="hasErrors"
      :class="{ 'has-xs-btm-marg': hasErrors && hasExtraSlot }"
      class="t-lh-b"
    >
      <li
        v-for="(message, index) in errorMessages"
        :key="message"
        :class="{ 'has-xs-btm-marg': index !== errorMessages.length - 1 }"
        class="has-text-error t-size-xs"
      >
        {{ message }}
      </li>
    </ul>
    <slot name="extra"></slot>
  </div>
</template>

<script>
import formElementMixin from '../mixins/element';

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
  },

  computed: {
    hasErrors() {
      return this.errorMessages.length > 0;
    },

    hasExtraSlot() {
      return !!this.$slots.extra;
    },

    ariaLabel() {
      if (this.showLabel) return null;

      return this.label;
    },
  },

  methods: {
    onInput(event) {
      this.$emit('input', event.target.value);
    },

    onPaste(event) {
      if (this.preventPaste) event.preventDefault();
    },
  },
};
</script>
