<template>
  <input
    :value="value"
    :name="name"
    :required="required"
    :pattern="pattern"
    :placeholder="placeholder"
    :class="getCssClasses()"
    type="text"
    @input="onInput($event.target.value)"
  >
</template>

<script>
import mapValueToElement from './mixins/mapValueToElement';
import updateSingleValueOnInput from './mixins/updateSingleValueOnInput';
import validateOnInput from '../mixins/form/validateOnInput';

export default {
  name: 'TextInput',

  mixins: [
    validateOnInput,
    mapValueToElement,
    updateSingleValueOnInput,
  ],

  props: {
    pattern: {
      type: [Boolean, String],
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
  },
};
</script>
