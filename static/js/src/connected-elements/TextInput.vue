<template>
  <input
    :value="value"
    :name="name"
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
    placeholder: {
      type: String,
      default: '',
    },
  },
};
</script>
