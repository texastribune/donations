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
import mapValueToElement from '../mixins/mapValueToElement';
import replaceSingleValueOnInput from '../mixins/replaceSingleValueOnInput';
import requiredField from '../mixins/requiredField';
import fieldWithPlaceholder from '../mixins/fieldWithPlaceholder';

export default {
  name: 'TextInput',

  mixins: [
    requiredField,
    mapValueToElement,
    fieldWithPlaceholder,
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
