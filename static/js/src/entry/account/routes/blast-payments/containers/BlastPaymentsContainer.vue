<template>
  <blast-payments :data="data" />
</template>

<script>
/* eslint-disable camelcase */

import parse from 'date-fns/parse';
import format from 'date-fns/format';
import isFuture from 'date-fns/is_future';

import BlastPayments from '../components/BlastPayments.vue';
import userMixin from '../../home/mixins/user';
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
        ({ date, amount, payment_type, credit_card }, index) => {
          let method = '';

          if (
            payment_type &&
            payment_type.toLowerCase() === CARD_PAYMENT_FLAG
          ) {
            method = `${credit_card.brand} ending in ${credit_card.last4}`;
          }

          return {
            id: index,
            date: parse(date),
            amount,
            method,
          };
        }
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
