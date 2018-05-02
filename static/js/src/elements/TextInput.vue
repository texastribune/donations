<template>
  <input
    :value="value"
    :name="name"
    :readonly="readonly"
    type="text"
    @input="updateValue($event.target.value)"
  >
</template>

<script>
import connectedFormElement from '../mixins/connectedFormElement';

export default {
  name: 'TextInput',

  mixins: [connectedFormElement],

  props: {
    readonly: {
      type: Boolean,
      default: false,
    },
  },
};
</script>
