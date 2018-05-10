<template>
  <input
    :value="value"
    :name="name"
    type="hidden"
  >
</template>

<script>
import mapValueToElement from './mixins/mapValueToElement';

export default {
  name: 'HiddenInput',

  mixins: [mapValueToElement],
};
</script>
