<template>
  <div>
    <error-view v-if="hasError" />
    <unverified-view v-else-if="isUnverified" />
    <router-view v-else />
  </div>
</template>

<script>
import { mapActions, mapState } from 'vuex';

import ErrorView from './ErrorView.vue';
import UnverifiedView from './UnverifiedView.vue';

export default {
  name: 'App',

  components: { ErrorView, UnverifiedView },

  computed: {
    ...mapState('context', ['hasError', 'isUnverified']),
  },

  methods: {
    ...mapActions('context', ['setError']),
  },

  errorCaptured() {
    this.setError(true);
  },
};
</script>
