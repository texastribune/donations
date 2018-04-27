<template>
  <input
    :value="value"
    type="text"
    @input="updateValue($event.target.value)"
  >
</template>

<script>
import connectedFormElement from '../mixins/connectedFormElement';

export default {
  name: 'Amount',

  mixins: [connectedFormElement],
};
</script>
