<template>
  <input
    :value="value"
    :name="name"
    :required="required"
    :class="getCssClasses()"
    readonly
    type="text"
  >
</template>

<script>
import mapValueToElement from './mixins/mapValueToElement';

export default {
  name: 'TextInput',

  mixins: [
    mapValueToElement,
  ],

  props: {
    required: {
      type: Boolean,
      default: true,
    },
  },
};
</script>
