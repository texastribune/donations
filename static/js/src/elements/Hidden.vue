<template>
  <input :value="value" :name="name" type="hidden" />
</template>

<script>
import connectedElement from './mixins/connectedElement';

console.log(process.env.AUTH0_DOMAIN);

export default {
  name: 'HiddenInput',

  mixins: [connectedElement],
};
</script>
