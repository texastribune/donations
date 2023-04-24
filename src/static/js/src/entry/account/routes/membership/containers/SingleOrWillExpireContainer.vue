<template>
  <transition name="has-fade">
    <single-or-will-expire
      v-if="shouldShow"
      :last-transaction="user.lastTransaction"
      :membership-expiration-date="user.membershipExpirationDate"
    />
  </transition>
</template>

<script>
import userMixin from '../../../store/user/mixin';

const SingleOrWillExpire = () =>
  import(/* webpackChunkName: "membership-single-or-will-expire" */ '../components/SingleOrWillExpire.vue');

export default {
  name: 'MembershipSingleOrWillExpireContainer',

  components: { SingleOrWillExpire },

  mixins: [userMixin],

  computed: {
    shouldShow() {
      const {
        isSingleDonor,
        isRecurringDonor,
        isCircleDonor,
        willExpire,
        isExpired,
      } = this.user;

      return (
        (isSingleDonor && !isExpired) ||
        ((isRecurringDonor || isCircleDonor) && willExpire)
      );
    },
  },
};
</script>
