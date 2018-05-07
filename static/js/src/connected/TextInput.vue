<template>
  <input
    :value="value"
    :name="name"
    :required="required"
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
    required: {
      type: Boolean,
      default: true,
    },
  },
};
</script>
