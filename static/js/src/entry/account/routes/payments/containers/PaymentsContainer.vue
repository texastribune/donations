<template>
  <payments :data="data" :is-expired="isExpired" :is-one-time="isOneTime" />
</template>

<script>
import parse from 'date-fns/parse';
import format from 'date-fns/format';
import isPast from 'date-fns/is_past';
import isFuture from 'date-fns/is_future';

import Payments from '../components/Payments.vue';
import userMixin from '../../home/mixins/user';
import addNumberCommas from '../../../utils/add-number-commas';

export default {
  name: 'PaymentsContainer',

  components: { Payments },

  mixins: [userMixin],

  computed: {
    isOneTime() {
      return !this.user.recurring_donor;
    },

    isExpired() {
      return isPast(parse(this.user.membership_expiration_date));
    },

    data() {
      const { transactions } = this.user;
      const relevantTransactions = transactions.filter(
        ({ type, date }) =>
          type.toLowerCase() === 'membership' && !isFuture(parse(date))
      );
      const withDateObjects = relevantTransactions.map(
        // eslint-disable-next-line camelcase
        ({ date, amount, payment_type, credit_card }, index) => ({
          id: index,
          date: parse(date),
          amount: addNumberCommas(amount),
          method:
            payment_type.toLowerCase() === 'credit card'
              ? `${credit_card.brand} ending in ${credit_card.last4}`
              : '',
        })
      );
      const sorted = withDateObjects.sort((a, b) => {
        if (a.date > b.date) return -1;
        if (a.date < b.date) return 1;
        return 0;
      });
      const formatted = sorted.map(item => ({
        ...item,
        date: format(item.date, 'MM/DD/YYYY'),
      }));

      return formatted;
    },
  },
};
</script>
