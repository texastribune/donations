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
import mapValueToElement from '../mixins/mapValueToElement';
import updateSingleStoreValue from '../mixins/updateSingleStoreValue';

export default {
  name: 'Email',

  mixins: [
    mapValueToElement,
    updateSingleStoreValue,
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
