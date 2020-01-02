<script>
/* eslint-disable camelcase */

import userMixin from '../../store/user/mixin';
import tokenUserMixin from '../../store/token-user/mixin';

export default {
  name: 'UserNavProvider',

  mixins: [userMixin, tokenUserMixin],

  computed: {
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
      isLoggedIn,
      showBlastLinks,
      showMembershipLink,
      showPaymentsLink,
    } = this;

    return this.$scopedSlots.default({
      isLoggedIn,
      showBlastLinks,
      showMembershipLink,
      showPaymentsLink,
    });
  },
};
</script>
