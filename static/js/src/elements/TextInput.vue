<template>
  <input
    :value="value"
    :name="name"
    type="text"
    @input="updateValue($event.target.value)"
  >
</template>

<script>
import connectedFormElement from '../mixins/connectedFormElement';

export default {
  name: 'TextInput',

  mixins: [connectedFormElement],
};
</script>
