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
  import(/* webpackChunkName: "summary-single-or-will-expire" */ '../components/SingleOrWillExpire.vue');

export default {
  name: 'SummarySingleOrWillExpireContainer',

  components: { SingleOrWillExpire },

  mixins: [userMixin],

  computed: {
    shouldShow() {
      const {
        isSingleDonor,
        isCircleDonor,
        isRecurringDonor,
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
