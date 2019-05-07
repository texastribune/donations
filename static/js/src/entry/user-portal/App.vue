<template>
  <div>
    <nav />
    <error-view v-if="context.hasError" />
    <router-view v-else />
  </div>
</template>

<script>
import ErrorView from './ErrorView.vue';
import contextMixin from './mixins/context';

export default {
  name: 'App',

  components: { ErrorView },

  mixins: [contextMixin],

  errorCaptured() {
    this.context.setError(true);
  },
};
</script>
