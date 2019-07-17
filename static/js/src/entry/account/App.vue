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
import ErrorView from './ErrorView.vue';
import UnverifiedView from './UnverifiedView.vue';
import contextMixin from './mixins/context';
import { UnverifiedError } from './errors';

export default {
  name: 'App',

  components: { ErrorView, UnverifiedView },

  mixins: [contextMixin],

  data() {
    return { error: null, isUnverified: false };
  },

  errorCaptured(err) {
    this.setAppIsFetching(false);

    if (err instanceof UnverifiedError) {
      this.isUnverified = true;
    } else {
      this.error = err;
    }
  },
};
</script>
