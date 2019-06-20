<template>
  <sustaining v-if="shouldShow" :next-transaction="nextTransaction" />
</template>

<script>
/* eslint-disable camelcase */

import isPast from 'date-fns/is_past';
import parse from 'date-fns/parse';

import Sustaining from '../components/Sustaining.vue';
import userMixin from '../../home/mixins/user';
import { CARD_PAYMENT_FLAG } from '../../../constants';

export default {
  name: 'SustainingContainer',

  components: { Sustaining },

  mixins: [userMixin],

  computed: {
    shouldShow() {
      const {
        recurring_donor,
        membership_expiration_date,
        is_mdev,
      } = this.user;
      const expired = isPast(parse(membership_expiration_date));

      return recurring_donor && !expired && !is_mdev;
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
