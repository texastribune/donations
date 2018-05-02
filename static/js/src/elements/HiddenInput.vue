<template>
  <input
    :value="value"
    :name="name"
    type="hidden"
  >
</template>

<script>
import connectedFormElement from '../mixins/connectedFormElement';

export default {
  name: 'HiddenInput',

  mixins: [connectedFormElement],
};
</script>
