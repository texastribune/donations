<template>
  <input
    :value="value"
    :name="name"
    readonly
    type="text"
  >
</template>

<script>
import mapValueToElement from '../mixins/mapValueToElement';

export default {
  name: 'TextInput',

  mixins: [mapValueToElement],
};
</script>
