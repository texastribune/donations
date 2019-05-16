<template>
  <div>
    <loader v-show="context.isFetching" />
    <loader v-if="isCheckingUser" :display="{ isOpaque: true }" />
    <main v-else class="has-white-off-bg">
      <div class="l-ump-container l-align-center-x">
        <div class="l-ump-grid">
          <div class="l-ump-grid__side is-hidden-until-bp-l"><side-nav /></div>
          <div class="l-ump-grid__content"><router-view /></div>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
import { mapActions } from 'vuex';

import contextMixin from '../../mixins/context';
import userMixin from '../../mixins/user';
import Loader from './components/Loader.vue';
import SideNav from './components/SideNav.vue';
import { LoggedOutError, Auth0Error } from '../../errors';

export default {
  name: 'Index',

  components: { Loader, SideNav },

  mixins: [contextMixin, userMixin],

  data() {
    return { isCheckingUser: true, data: [] };
  },

  mounted() {
    this.getUserOrRedirect();
  },

  methods: {
    ...mapActions('user', ['getUser']),

    async getUserOrRedirect() {
      try {
        await this.getUser();
        this.isCheckingUser = false;
      } catch (err) {
        if (err instanceof LoggedOutError) {
          this.user.logIn();
        } else if (err instanceof Auth0Error) {
          this.isCheckingUser = false;
          this.context.setError(true);
        }
      }
    },
  },
};
</script>
