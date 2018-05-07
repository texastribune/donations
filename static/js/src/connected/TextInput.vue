<template>
  <input
    :value="value"
    :name="name"
    :required="required"
    :maxlength="maxlength"
    :pattern="pattern"
    :class="getClasses()"
    type="text"
    @input="onInput($event.target.value)"
  >
</template>

<script>
import mapValueToElement from '../mixins/mapValueToElement';
import replaceSingleValueOnInput from '../mixins/replaceSingleValueOnInput';

export default {
  name: 'TextInput',

  mixins: [
    mapValueToElement,
    replaceSingleValueOnInput,
  ],

  props: {
    maxlength: {
      type: [Boolean, String],
      default: false,
    },

    pattern: {
      type: [Boolean, String],
      default: false,
    },

    required: {
      type: Boolean,
      default: true,
    },
  },
};
</script>
