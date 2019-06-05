<template>
  <div>
    <error-view v-if="hasError" />
    <router-view v-else />
  </div>
</template>

<script>
import { mapActions, mapState } from 'vuex';

import ErrorView from './ErrorView.vue';

export default {
  name: 'App',

  components: { ErrorView },

  computed: {
    ...mapState('context', ['hasError']),
  },

  methods: {
    ...mapActions('context', ['setError']),
  },

  errorCaptured() {
    this.setError(true);
  },
};
</script>
