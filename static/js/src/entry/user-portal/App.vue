<template>
  <div>
    <nav style="height:45px;background:#fff;border-bottom:1px solid #dcdcdc" />
    <error-view v-if="context.hasError" />
    <router-view v-else />
    <footer style="height:300px;background:#222;" />
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
