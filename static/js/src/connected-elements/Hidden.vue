<template>
  <input :value="value" :name="name" type="hidden" />
</template>

<script>
import connectedElement from './mixins/connectedElement';

export default {
  name: 'HiddenInput',

  mixins: [connectedElement],
};
</script>
