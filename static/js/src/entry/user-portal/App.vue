<template>
  <div>
    <loader v-show="context.isFetching" />
    <loader v-if="isCheckingUser" :display="{ isOpaque: true }" />
    <error-view v-else-if="context.hasError" />
    <router-view v-else />
  </div>
</template>

<script>
import { mapActions } from 'vuex';

import ErrorView from './ErrorView.vue';
import contextMixin from './mixins/context';
import { Auth0Error } from './errors';

export default {
  name: 'App',

  components: { ErrorView },

  mixins: [contextMixin],

  data() {
    return { isCheckingUser: true };
  },

  mounted() {
    this.getUserOrRedirect();
  },

  methods: {
    ...mapActions('user', ['getUser']),

    async getUserOrRedirect() {
      try {
        await this.getUser();
      } catch (err) {
        if (err instanceof Auth0Error) {
          this.context.setError(true);
        }
      } finally {
        this.isCheckingUser = false;
      }
    },
  },

  errorCaptured() {
    this.context.setError(true);
  },
};
</script>
