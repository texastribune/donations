<template>
  <transition name="has-fade">
    <recurring-or-circle
      v-if="shouldShow"
      :next-transaction="user.nextTransaction"
      :first-name="user.firstName"
      :last-name="user.lastName"
      :email="user.email"
      :recurring-transactions="user.recurringTransactions"
      :can-view-as="tokenUser.canViewAs"
    />
  </transition>
</template>

<script>
import userMixin from '../../../store/user/mixin';
import tokenUserMixin from '../../../store/token-user/mixin';

const RecurringOrCircle = () =>
  import(/* webpackChunkName: "membership-recurring-or-circle" */ '../components/RecurringOrCircle.vue');

export default {
  name: 'MembershipRecurringOrCircleContainer',

  components: { RecurringOrCircle },

  mixins: [userMixin, tokenUserMixin],

  computed: {
    shouldShow() {
      const {
        isCircleDonor,
        isRecurringDonor,
        willExpire,
        isExpired,
      } = this.user;

      return (isCircleDonor || isRecurringDonor) && !isExpired && !willExpire;
    },
  },
};
</script>
