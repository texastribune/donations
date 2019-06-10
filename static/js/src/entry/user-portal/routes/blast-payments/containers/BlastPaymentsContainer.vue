<template>
  <blast-payments :data="data" />
</template>

<script>
import parse from 'date-fns/parse';
import format from 'date-fns/format';
import isFuture from 'date-fns/is_future';

import BlastPayments from '../components/BlastPayments.vue';
import userMixin from '../../home/mixins/user';
import addNumberCommas from '../../../utils/add-number-commas';

export default {
  name: 'BlastPaymentsContainer',

  components: { BlastPayments },

  mixins: [userMixin],

  computed: {
    data() {
      const { transactions } = this.user;
      const relevantTransactions = transactions.filter(
        ({ type, date }) => type === 'blast' && !isFuture(parse(date))
      );
      const withDateObjects = relevantTransactions.map(
        ({ date, amount, credit_card: { brand, last4 } }, index) => ({
          id: index,
          date: parse(date),
          amount: addNumberCommas(amount),
          method: `${brand} ending in ${last4}`,
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
