<template>
  <detail :data="data" :is-cancelled="isCancelled" />
</template>

<script>
/* eslint-disable camelcase */

import parse from 'date-fns/parse';
import isFuture from 'date-fns/is_future';

import Detail from '../components/Detail.vue';
import userMixin from '../../../store/user/mixin';
import { BLAST_PAYMENT_FLAG, CARD_PAYMENT_FLAG } from '../../../constants';

export default {
  name: 'BlastPaymentsDetailContainer',

  components: { Detail },

  mixins: [userMixin],

  computed: {
    isCancelled() {
      return this.user.is_former_blast_subscriber;
    },

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
            method = `${credit_card.brand} ${credit_card.last4}`;
          }

          return {
            id: index,
            date: parse(date),
            amount,
            method,
          };
        }
      );

      return withDateObjects.sort((a, b) => {
        if (a.date > b.date) return -1;
        if (a.date < b.date) return 1;
        return 0;
      });
    },
  },
};
</script>
