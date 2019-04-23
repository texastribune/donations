<template>
  <div v-if="context.hasError">Oh no! An error occurred.</div>
  <router-view v-else />
</template>

<script>
import contextMixin from './mixins/context';

export default {
  name: 'App',

  mixins: [contextMixin],
};
</script>
