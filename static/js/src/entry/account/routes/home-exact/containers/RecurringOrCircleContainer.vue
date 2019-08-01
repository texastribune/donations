<template>
  <transition name="has-fade">
    <recurring-or-circle
      v-if="shouldShow"
      :next-transaction="nextTransaction"
    />
  </transition>
</template>

<script>
/* eslint-disable camelcase */

import userMixin from '../../../store/user/mixin';
import { CARD_PAYMENT_FLAG } from '../../../constants';

const RecurringOrCircle = () =>
  import(/* webpackChunkName: "summary-recurring-or-circle" */ '../components/RecurringOrCircle.vue');

export default {
  name: 'SummaryRecurringOrCircleContainer',

  components: { RecurringOrCircle },

  mixins: [userMixin],

  computed: {
    shouldShow() {
      const {
        is_recurring_donor,
        is_circle_donor,
        is_expired,
        will_expire,
      } = this.user;

      return (
        (is_recurring_donor || is_circle_donor) && !is_expired && !will_expire
      );
    },

    nextTransaction() {
      const {
        next_transaction: { amount, period, date, payment_type, credit_card },
      } = this.user;

      const data = {
        amount,
        date,
        period,
      };

      if (payment_type && payment_type.toLowerCase() === CARD_PAYMENT_FLAG) {
        data.last4 = credit_card.last4;
      }

      return data;
    },
  },
};
</script>
