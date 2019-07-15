<template>
  <side-nav
    :show-blast-links="showBlastLinks"
    :show-membership-link="showMembershipLink"
    :show-payments-link="showPaymentsLink"
    :show-route-links="showRouteLinks"
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

  props: {
    showRouteLinks: {
      type: Boolean,
      required: true,
    },
  },

  computed: {
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

      const {
        is_single_donor,
        is_recurring_donor,
        is_circle_donor,
      } = this.user;

      return is_single_donor || is_recurring_donor || is_circle_donor;
    },

    showPaymentsLink() {
      if (!this.showRouteLinks) return false;

      const { never_given } = this.user;

      return !never_given;
    },
  },
};
</script>
