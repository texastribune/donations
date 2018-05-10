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
import updateSingleStoreValue from '../mixins/updateSingleStoreValue';

export default {
  name: 'TextInput',

  mixins: [
    mapValueToElement,
    updateSingleStoreValue,
  ],

  props: {
    pattern: {
      type: [Boolean, String],
      default: false,
    },

    placeholder: {
      type: String,
      default: '',
    },

    required: {
      type: Boolean,
      default: true,
    },
  },
};
</script>
