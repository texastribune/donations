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

  render() {
    const {
      userFetchComplete,
      showBlastLinks,
      showMembershipLink,
      showPaymentsLink,
      isLoggedIn,
    } = this;

    return this.$scopedSlots.default({
      userFetchComplete,
      showBlastLinks,
      showMembershipLink,
      showPaymentsLink,
      isLoggedIn,
    });
  },
};
</script>
