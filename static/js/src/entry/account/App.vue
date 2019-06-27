<template>
  <div>
    <loader v-if="appIsFetching" />

    <error-view v-if="error" />
    <unverified-view v-else-if="isUnverified" />
    <router-view v-else :parent-is-fetching="false" />
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
    ...mapState('context', ['error', 'isUnverified', 'appIsFetching']),
  },

  methods: {
    ...mapActions('context', ['setError', 'setAppIsFetching']),
  },

  errorCaptured(err) {
    this.setAppIsFetching(false);
    this.setError(err);
  },
};
</script>
