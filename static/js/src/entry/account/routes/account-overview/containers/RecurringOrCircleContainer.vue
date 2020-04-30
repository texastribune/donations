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
  import(/* webpackChunkName: "summary-recurring-or-circle" */ '../components/RecurringOrCircle.vue');

export default {
  name: 'SummaryRecurringOrCircleContainer',

  components: { RecurringOrCircle },

  mixins: [userMixin],

  computed: {
    shouldShow() {
      const {
        isRecurringDonor,
        isCircleDonor,
        isExpired,
        willExpire,
      } = this.user;

      return (isRecurringDonor || isCircleDonor) && !isExpired && !willExpire;
    },
  },
};
</script>
