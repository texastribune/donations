<template>
  <transition name="has-fade">
    <recurring-or-circle
      v-if="shouldShow"
      :next-transaction="user.nextTransaction"
    />
  </transition>
</template>

<script>
import userMixin from '../../../store/user/mixin';

const RecurringOrCircle = () =>
  import(/* webpackChunkName: "membership-recurring-or-circle" */ '../components/RecurringOrCircle.vue');

export default {
  name: 'MembershipRecurringOrCircleContainer',

  components: { RecurringOrCircle },

  mixins: [userMixin],

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
