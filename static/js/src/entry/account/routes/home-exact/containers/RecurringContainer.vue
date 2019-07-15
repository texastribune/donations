<template>
  <transition name="has-fade">
    <recurring v-if="shouldShow" :next-transaction="nextTransaction" />
  </transition>
</template>

<script>
/* eslint-disable camelcase */

import userMixin from '../../home/mixins/user';
import { CARD_PAYMENT_FLAG } from '../../../constants';

const Recurring = () =>
  import(/* webpackChunkName: "recurring-summary" */ '../components/Recurring.vue');

export default {
  name: 'RecurringContainer',

  components: { Recurring },

  mixins: [userMixin],

  computed: {
    shouldShow() {
      const { is_recurring_donor, is_expired } = this.user;

      return is_recurring_donor && !is_expired;
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
