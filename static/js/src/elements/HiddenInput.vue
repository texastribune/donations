<template>
  <input
    :value="value"
    :name="identifier"
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
