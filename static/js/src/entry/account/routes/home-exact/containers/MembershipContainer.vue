<template>
  <membership
    v-if="isRecurringAndNotExpired"
    :next-transaction="nextTransaction"
  />
</template>

<script>
/* eslint-disable camelcase */

import isPast from 'date-fns/is_past';
import format from 'date-fns/format';
import parse from 'date-fns/parse';

import Membership from '../components/Membership.vue';
import userMixin from '../../home/mixins/user';
import { CARD_PAYMENT_FLAG } from '../../../constants';

export default {
  name: 'MembershipContainer',

  components: { Membership },

  mixins: [userMixin],

  computed: {
    isRecurringAndNotExpired() {
      // eslint-disable-next-line camelcase
      const { recurring_donor, membership_expiration_date } = this.user;
      const expired = isPast(parse(membership_expiration_date));

      // eslint-disable-next-line camelcase
      return recurring_donor && !expired;
    },

    nextTransaction() {
      const {
        next_transaction: { amount, period, date, payment_type, credit_card },
      } = this.user;
      const data = {
        amount,
        date: format(parse(date), 'MMMM D, YYYY'),
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
