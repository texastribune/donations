<template>
  <input
    :value="value"
    :name="name"
    :required="required"
    :placeholder="placeholder"
    :class="getCssClasses()"
    type="email"
    @input="onInput($event.target.value)"
  >
</template>

<script>
import mapValueToElement from './mixins/mapValueToElement';
import updateSingleValueOnInput from './mixins/updateSingleValueOnInput';
import validateOnInput from '../mixins/form/validateOnInput';

export default {
  name: 'Email',

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

    required: {
      type: Boolean,
      default: true,
    },
  },
};
</script>
