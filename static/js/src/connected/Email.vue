<template>
  <input
    :value="value"
    :name="name"
    :required="required"
    type="email"
    @input="onInput($event.target.value)"
  >
</template>

<script>
import mapValueToElement from '../mixins/mapValueToElement';
import replaceSingleValueOnInput from '../mixins/replaceSingleValueOnInput';

export default {
  name: 'Email',

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
