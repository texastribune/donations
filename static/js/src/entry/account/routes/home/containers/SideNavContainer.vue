<template>
  <side-nav
    :show-blast-links="showBlastLinks"
    :show-membership-links="showMembershipLinks"
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

    showMembershipLinks() {
      return !this.user.never_given;
    },
  },
};
</script>
