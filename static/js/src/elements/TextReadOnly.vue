<template>
  <input
    :value="value"
    :name="name"
    :class="getCssClasses()"
    readonly
    type="text"
  >
</template>

<script>
import connectedElement from './mixins/connectedElement';

export default {
  name: 'TextInput',

  mixins: [connectedElement],
};
</script>
