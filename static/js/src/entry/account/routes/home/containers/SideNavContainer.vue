<template>
  <side-nav
    :show-blast-links="showBlastLinks"
    :show-membership-link="showMembershipLink"
    :show-payments-link="showPaymentsLink"
  />
</template>

<script>
/* eslint-disable camelcase */

import SideNav from '../components/SideNav.vue';
import userMixin from '../mixins/user';

export default {
  name: 'SideNavContainer',

  components: { SideNav },

  mixins: [userMixin],

  computed: {
    showBlastLinks() {
      const {
        is_former_blast_subscriber,
        is_current_blast_subscriber,
      } = this.user;

      return is_former_blast_subscriber || is_current_blast_subscriber;
    },

    showMembershipLink() {
      const { never_given, is_mdev } = this.user;

      return !never_given && !is_mdev;
    },

    showPaymentsLink() {
      const { never_given } = this.user;

      return !never_given;
    },
  },
};
</script>
