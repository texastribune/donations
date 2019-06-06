<template>
  <expired
    v-if="isRecurringAndExpired"
    :last-transaction="lastTransaction"
    :expiration-date="expirationDate"
  />
</template>

<script>
import isPast from 'date-fns/is_past';
import format from 'date-fns/format';
import parse from 'date-fns/parse';

import Expired from '../components/Expired.vue';
import addNumberCommas from '../../../utils/add-number-commas';
import userMixin from '../../../mixins/user';

export default {
  name: 'ExpiredContainer',

  components: { Expired },

  mixins: [userMixin],

  computed: {
    isRecurringAndExpired() {
      // eslint-disable-next-line camelcase
      const { active_recurring_donor, membership_expiration_date } = this.user;
      const expired = isPast(parse(membership_expiration_date));

      // eslint-disable-next-line camelcase
      return active_recurring_donor && expired;
    },

    expirationDate() {
      // eslint-disable-next-line camelcase
      const { membership_expiration_date } = this.user;

      return format(parse(membership_expiration_date), 'MMMM D, YYYY');
    },

    lastTransaction() {
      const {
        last_transaction: {
          amount,
          period,
          date,
          credit_card: { last4 },
        },
      } = this.user;

      return {
        amount: addNumberCommas(amount),
        date: format(parse(date), 'MMMM D, YYYY'),
        last4,
        period,
      };
    },
  },
};
</script>
