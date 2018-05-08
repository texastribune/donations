<template>
  <input
    :value="value"
    :name="name"
    :required="required"
    :pattern="pattern"
    :class="classes"
    type="text"
    @input="onInput($event.target.value)"
  >
</template>

<script>
import mapValueToElement from '../mixins/mapValueToElement';
import replaceSingleValueOnInput from '../mixins/replaceSingleValueOnInput';
import requiredField from '../mixins/requiredField';

export default {
  name: 'TextInput',

  mixins: [
    requiredField,
    mapValueToElement,
    replaceSingleValueOnInput,
  ],

  props: {
    pattern: {
      type: [Boolean, String],
      default: false,
    },
  },
};
</script>
