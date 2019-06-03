<template>
  <div>
    <loader v-show="context.isFetching" />
    <error-view v-if="context.hasError" />
    <router-view v-else />
  </div>
</template>

<script>
import Loader from './components/Loader.vue';
import ErrorView from './ErrorView.vue';
import contextMixin from './mixins/context';

export default {
  name: 'App',

  components: { ErrorView, Loader },

  mixins: [contextMixin],

  errorCaptured() {
    this.context.setError(true);
  },
};
</script>
