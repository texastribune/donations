<template>
  <fieldset>
    <input
      v-for="option in options"
      :key="option.id"
      :value="option.value"
      :name="name"
      :checked="value === option.value"
      type="radio"
      @input="onInput($event.target.value)"
    >
  </fieldset>
</template>

<script>
import mapValueToElement from '../mixins/mapValueToElement';
import replaceSingleValueOnInput from '../mixins/replaceSingleValueOnInput';

export default {
  name: 'Frequency',

  mixins: [
    mapValueToElement,
    replaceSingleValueOnInput,
  ],

  props: {
    options: {
      type: Array,
      required: true,
    },
  },
};
</script>
