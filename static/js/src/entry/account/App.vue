<template>
  <div>
    <transition name="has-fade">
      <app-loader v-show="showLoader" />
    </transition>

    <unverified-view v-if="showUnverified" />
    <error-view v-else-if="showError" />
    <router-view v-else :parent-route-is-fetching="false" />
  </div>
</template>

<script>
import ErrorView from './ErrorView.vue';
import UnverifiedView from './UnverifiedView.vue';
import AppLoader from './components/AppLoader.vue';
import contextMixin from './store/context/mixin';
import { CONTEXT_TYPES } from './store/types';
import { UnverifiedError } from './errors';

export default {
  name: 'App',

  components: { ErrorView, UnverifiedView, AppLoader },

  mixins: [contextMixin],

  computed: {
    showLoader() {
      return this.context.isFetching && !this.context.error;
    },

    showUnverified() {
      return this.context.error instanceof UnverifiedError;
    },

    showError() {
      return !!this.context.error;
    },
  },

  errorCaptured(err) {
    this[CONTEXT_TYPES.setError](err);
  },
};
</script>
