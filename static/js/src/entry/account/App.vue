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
import { UnverifiedError } from './errors';
import { TITLE_SUFFIX } from './constants';

export default {
  name: 'App',

  components: { ErrorView, UnverifiedView, AppLoader },

  mixins: [contextMixin],

  computed: {
    showLoader() {
      return this.appIsFetching && !this.error;
    },

    showUnverified() {
      return this.error instanceof UnverifiedError;
    },

    showError() {
      return !!this.error;
    },
  },

  watch: {
    error(newError) {
      if (newError) {
        if (newError instanceof UnverifiedError) {
          this.setTitle('Unverified email address');
        } else {
          this.setTitle('Error');
        }
      }
    },
  },

  methods: {
    setTitle(title) {
      document.title = `${title} ${TITLE_SUFFIX}`;
    },
  },

  errorCaptured(err) {
    this.setError(err);
  },
};
</script>
