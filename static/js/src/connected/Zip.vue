<template>
  <input
    :value="value"
    :name="name"
    :required="required"
    type="text"
    maxlength="5"
    pattern="[0-9]"
    @input="onInput($event.target.value)"
  >
</template>

<script>
import mapValueToElement from '../mixins/mapValueToElement';
import replaceSingleValueOnInput from '../mixins/replaceSingleValueOnInput';

export default {
  name: 'Zip',

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
