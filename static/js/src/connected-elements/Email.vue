<template>
  <input
    :value="value"
    :name="name"
    :placeholder="placeholder"
    :class="getCssClasses()"
    type="email"
    @input="updateSingleValue($event.target.value)"
    @blur="validate($event.target.value)"
  >
</template>

<script>
import mapValueToElement from './mixins/mapValueToElement';
import updateSingleValue from './mixins/updateSingleValue';
import validateOnInput from '../mixins/form/validateOnInput';

export default {
  name: 'Email',

  mixins: [
    validateOnInput,
    mapValueToElement,
    updateSingleValue,
  ],

  props: {
    placeholder: {
      type: String,
      default: '',
    },
  },
};
</script>
