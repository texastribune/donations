<template>
  <input
    :value="value"
    :name="name"
    :placeholder="placeholder"
    :class="getCssClasses()"
    type="email"
    @input="updateSingleValue($event.target.value)"
  >
</template>

<script>
import connectedElement from './mixins/connectedElement';

export default {
  name: 'Email',

  mixins: [connectedElement],

  props: {
    placeholder: {
      type: String,
      default: '',
    },
  },
};
</script>
