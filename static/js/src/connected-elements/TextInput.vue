<template>
  <input
    :value="value"
    :name="name"
    :placeholder="placeholder"
    :class="getCssClasses()"
    type="text"
    @input="updateSingleValue($event.target.value)"
  >
</template>

<script>
import mapValueToElement from './mixins/mapValueToElement';
import updateSingleValue from './mixins/updateSingleValue';

export default {
  name: 'TextInput',

  mixins: [
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
