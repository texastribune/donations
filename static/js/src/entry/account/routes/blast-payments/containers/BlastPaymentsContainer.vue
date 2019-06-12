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
import { BLAST_PAYMENT_FLAG, CARD_PAYMENT_FLAG } from '../../../constants';

export default {
  name: 'BlastPaymentsContainer',

  components: { BlastPayments },

  mixins: [userMixin],

  computed: {
    data() {
      const { transactions } = this.user;
      const relevantTransactions = transactions.filter(
        ({ type, date }) =>
          type.toLowerCase() === BLAST_PAYMENT_FLAG && !isFuture(parse(date))
      );
      const withDateObjects = relevantTransactions.map(
        // eslint-disable-next-line camelcase
        ({ date, amount, payment_type, credit_card }, index) => ({
          id: index,
          date: parse(date),
          amount: addNumberCommas(amount),
          method:
            payment_type.toLowerCase() === CARD_PAYMENT_FLAG
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
