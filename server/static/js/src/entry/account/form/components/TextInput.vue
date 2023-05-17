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

    <div v-show="hasErrors" :class="{ 'has-xs-btm-marg': hasExtraSlot }">
      <errors :error-messages="errorMessages" />
    </div>

    <slot name="extra"></slot>
  </div>
</template>

<script>
import formElementMixin from '../mixins/element';

import Errors from './Errors.vue';

export default {
  name: 'TextInput',

  components: { Errors },

  mixins: [formElementMixin],

  props: {
    value: {
      type: String,
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
