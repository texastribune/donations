<template>
  <input :value="value" :name="name" type="hidden" />
</template>

<script>
import connectedElement from './mixins/connected-element';

export default {
  name: 'HiddenInput',

  mixins: [connectedElement],
};
</script>
