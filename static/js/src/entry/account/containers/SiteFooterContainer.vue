<template>
  <site-footer
    :show-route-links="showRouteLinks"
    :show-blast-links="showBlastLinks"
    :show-membership-links="showMembershipLinks"
  />
</template>

<script>
/* eslint-disable camelcase */

import SiteFooter from '../components/SiteFooter.vue';
import userMixin from '../routes/home/mixins/user';

export default {
  name: 'SiteFooterContainer',

  components: { SiteFooter },

  mixins: [userMixin],

  props: {
    showRouteLinks: {
      type: Boolean,
      default: true,
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

    showMembershipLinks() {
      if (!this.showRouteLinks) return false;
      return !this.user.never_given;
    },
  },
};
</script>
