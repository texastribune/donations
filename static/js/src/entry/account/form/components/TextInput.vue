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
      :aria-label="showLabel ? false : label"
      :aria-invalid="showErrors"
      :readonly="readOnly"
      :class="{
        'is-invalid': showErrors,
        'has-xxxs-btm-marg': showErrors || (!showErrors && !!$slots.extra),
      }"
      class="c-text-input__input l-display-block l-width-full has-text-gray-dark t-lh-b"
      type="text"
      @input="onInput"
      @paste="onPaste"
    />
    <ul
      v-show="showErrors"
      :class="{ 'has-xs-btm-marg': showErrors && !!$slots.extra }"
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

    showErrorImmediately: {
      type: Boolean,
      default: true,
    },
  },

  computed: {
    showErrors() {
      const { valid, pristine, showErrorImmediately } = this;

      return (
        (!valid && !showErrorImmediately && !pristine) ||
        (!valid && showErrorImmediately)
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
