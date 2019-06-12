<template>
  <membership-expired
    v-if="isRecurringAndExpired"
    :last-transaction="lastTransaction"
    :expiration-date="expirationDate"
  />
</template>

<script>
/* eslint-disable camelcase */

import isPast from 'date-fns/is_past';
import format from 'date-fns/format';
import parse from 'date-fns/parse';

import MembershipExpired from '../components/MembershipExpired.vue';
import userMixin from '../../home/mixins/user';
import { CARD_PAYMENT_FLAG } from '../../../constants';

export default {
  name: 'MembershipExpiredContainer',

  components: { MembershipExpired },

  mixins: [userMixin],

  computed: {
    isRecurringAndExpired() {
      const { recurring_donor, membership_expiration_date } = this.user;
      const expired = isPast(parse(membership_expiration_date));

      // eslint-disable-next-line camelcase
      return recurring_donor && expired;
    },

    expirationDate() {
      const { membership_expiration_date } = this.user;

      return format(parse(membership_expiration_date), 'MMMM D, YYYY');
    },

    lastTransaction() {
      const {
        last_transaction: { amount, period, date, payment_type, credit_card },
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
