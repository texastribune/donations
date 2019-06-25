<template>
  <sustaining v-if="shouldShow" :next-transaction="nextTransaction" />
</template>

<script>
/* eslint-disable camelcase */

import Sustaining from '../components/Sustaining.vue';
import userMixin from '../../home/mixins/user';
import { CARD_PAYMENT_FLAG } from '../../../constants';

export default {
  name: 'SustainingContainer',

  components: { Sustaining },

  mixins: [userMixin],

  computed: {
    shouldShow() {
      const { is_recurring_donor, is_expired, is_mdev } = this.user;

      return is_recurring_donor && !is_expired && !is_mdev;
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
