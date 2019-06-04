<template>
  <div>
    <loader v-show="isFetching" />
    <error-view v-if="hasError" />
    <router-view v-else />
  </div>
</template>

<script>
import { mapActions, mapState } from 'vuex';

import Loader from './components/Loader.vue';
import ErrorView from './ErrorView.vue';

export default {
  name: 'App',

  components: { ErrorView, Loader },

  computed: {
    ...mapState('context', ['hasError', 'isFetching']),
  },

  methods: {
    ...mapActions('context', ['setError']),
  },

  errorCaptured() {
    this.setError(true);
  },
};
</script>
