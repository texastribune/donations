<template>
  <div>
    <transition name="has-fade">
      <app-loader v-show="showLoader" />
    </transition>

    <error-view v-if="showError" />
    <router-view v-else />
  </div>
</template>

<script>
import contextMixin from './store/context/mixin';

import ErrorView from './ErrorView.vue';
import AppLoader from './components/AppLoader.vue';

import logError from './utils/log-error';

import { CONTEXT_TYPES } from './store/types';

export default {
  name: 'App',

  components: { ErrorView, AppLoader },

  mixins: [contextMixin],

  computed: {
    showLoader() {
      return this.context.isFetching && !this.context.error;
    },

    showError() {
      return !!this.context.error;
    },
  },

  errorCaptured(err) {
    this[CONTEXT_TYPES.setError](err);

    logError({ err });

    return false;
  },
};
</script>
