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
import connectedElement from './mixins/connectedElement';

export default {
  name: 'TextInput',

  mixins: [connectedElement],

  props: {
    placeholder: {
      type: String,
      default: '',
    },
  },
};
</script>
