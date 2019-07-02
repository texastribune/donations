<template>
  <div>
    <transition name="has-fade">
      <app-loader v-show="appIsFetching" />
    </transition>

    <error-view v-if="error" />
    <unverified-view v-else-if="isUnverified" />
    <router-view v-else :parent-route-is-fetching="false" />
  </div>
</template>

<script>
import { mapState } from 'vuex';

import ErrorView from './ErrorView.vue';
import UnverifiedView from './UnverifiedView.vue';
import contextMixin from './mixins/context';

export default {
  name: 'App',

  components: { ErrorView, UnverifiedView },

  mixins: [contextMixin],

  computed: {
    ...mapState('context', ['error', 'isUnverified']),
  },

  errorCaptured(err) {
    this.setAppIsFetching(false);
    this.setError(err);
  },
};
</script>
