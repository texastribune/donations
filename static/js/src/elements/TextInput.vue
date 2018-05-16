<template>
  <input
    :value="value"
    :name="name"
    :maxlength="maxlength"
    :placeholder="placeholder"
    :class="classes"
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

    maxlength: {
      type: [String, Boolean],
      default: false,
    },
  },
};
</script>
