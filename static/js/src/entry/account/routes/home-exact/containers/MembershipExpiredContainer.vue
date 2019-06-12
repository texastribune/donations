<template>
  <membership-expired
    v-if="isRecurringAndExpired"
    :last-transaction="lastTransaction"
    :expiration-date="expirationDate"
  />
</template>

<script>
import isPast from 'date-fns/is_past';
import format from 'date-fns/format';
import parse from 'date-fns/parse';

import MembershipExpired from '../components/MembershipExpired.vue';
import addNumberCommas from '../../../utils/add-number-commas';
import userMixin from '../../home/mixins/user';

export default {
  name: 'MembershipExpiredContainer',

  components: { MembershipExpired },

  mixins: [userMixin],

  computed: {
    isRecurringAndExpired() {
      // eslint-disable-next-line camelcase
      const { recurring_donor, membership_expiration_date } = this.user;
      const expired = isPast(parse(membership_expiration_date));

      // eslint-disable-next-line camelcase
      return recurring_donor && expired;
    },

    expirationDate() {
      // eslint-disable-next-line camelcase
      const { membership_expiration_date } = this.user;

      return format(parse(membership_expiration_date), 'MMMM D, YYYY');
    },

    lastTransaction() {
      const {
        // eslint-disable-next-line camelcase
        last_transaction: { amount, period, date, payment_type, credit_card },
      } = this.user;
      const data = {
        amount: addNumberCommas(amount),
        date: format(parse(date), 'MMMM D, YYYY'),
        period,
      };

      if (payment_type.toLowerCase() === 'credit card') {
        data.last4 = credit_card.last4;
      }

      return data;
    },
  },
};
</script>
