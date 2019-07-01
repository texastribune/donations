<template>
  <nav-bar
    :show-route-links="showRouteLinks"
    :show-blast-links="showBlastLinks"
    :show-membership-link="showMembershipLink"
    :is-logged-in="isLoggedIn"
  />
</template>

<script>
/* eslint-disable camelcase */

import NavBar from '../components/NavBar.vue';
import userMixin from '../routes/home/mixins/user';
import tokenUserMixin from '../mixins/token-user';

export default {
  name: 'NavBarContainer',

  components: { NavBar },

  mixins: [userMixin, tokenUserMixin],

  props: {
    showRouteLinks: {
      type: Boolean,
      default: true,
    },
  },

  computed: {
    isLoggedIn() {
      return !!this.accessToken;
    },

    showBlastLinks() {
      if (!this.showRouteLinks) return false;

      const {
        is_former_blast_subscriber,
        is_current_blast_subscriber,
      } = this.user;

      return is_former_blast_subscriber || is_current_blast_subscriber;
    },

    showMembershipLink() {
      if (!this.showRouteLinks) return false;

      const { never_given, is_mdev } = this.user;

      return !never_given && !is_mdev;
    },
  },
};
</script>
