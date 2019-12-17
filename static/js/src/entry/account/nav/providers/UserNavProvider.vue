<template>
  <token-user-nav-provider v-slot="slotProps">
    <slot
      :show-blast-links="showBlastLinks"
      :show-membership-link="showMembershipLink"
      :show-payments-link="showPaymentsLink"
      :is-logged-in="slotProps.isLoggedIn"
    ></slot>
  </token-user-nav-provider>
</template>

<script>
/* eslint-disable camelcase */

import userMixin from '../../store/user/mixin';
import TokenUserNavProvider from './TokenUserNavProvider.vue';

export default {
  name: 'UserNavProvider',

  components: { TokenUserNavProvider },

  mixins: [userMixin],

  computed: {
    showBlastLinks() {
      return !!this.user.is_blast_subscriber;
    },

    showMembershipLink() {
      const {
        is_single_donor,
        is_recurring_donor,
        is_circle_donor,
      } = this.user;

      return !!(is_single_donor || is_recurring_donor || is_circle_donor);
    },

    showPaymentsLink() {
      const { never_given } = this.user;

      return !never_given;
    },
  },
};
</script>
