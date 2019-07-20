<template>
  <div>
    <slot
      show-home-link
      :user-fetch-complete="userFetchComplete"
      :show-blast-links="showBlastLinks"
      :show-membership-link="showMembershipLink"
      :show-payments-link="showPaymentsLink"
      :is-logged-in="isLoggedIn"
    ></slot>
  </div>
</template>

<script>
/* eslint-disable camelcase */

import userMixin from '../../store/user/mixin';
import tokenUserMixin from '../../store/token-user/mixin';

export default {
  name: 'UserNavContainer',

  mixins: [userMixin, tokenUserMixin],

  computed: {
    userFetchComplete() {
      return Object.keys(this.user).length > 0;
    },

    isLoggedIn() {
      return !!this.accessToken;
    },

    showBlastLinks() {
      const {
        is_former_blast_subscriber,
        is_current_blast_subscriber,
      } = this.user;

      return !!(is_former_blast_subscriber || is_current_blast_subscriber);
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
