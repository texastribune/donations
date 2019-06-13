<template>
  <payments
    :data="data"
    :is-expired="isExpired"
    :is-one-time="isOneTime"
    :total-gifts-last-year="totalGiftsLastYear"
    @setError="setError"
  />
</template>

<script>
/* eslint-disable camelcase */

import parse from 'date-fns/parse';
import format from 'date-fns/format';
import isPast from 'date-fns/is_past';
import isFuture from 'date-fns/is_future';
import { mapActions } from 'vuex';

import Payments from '../components/Payments.vue';
import userMixin from '../../home/mixins/user';
import { MEMBERSHIP_PAYMENT_FLAG, CARD_PAYMENT_FLAG } from '../../../constants';

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

    totalGiftsLastYear() {
      return this.user.total_gifts_last_year;
    },

    data() {
      const { transactions } = this.user;
      const relevantTransactions = transactions.filter(
        ({ type, date }) =>
          type.toLowerCase() === MEMBERSHIP_PAYMENT_FLAG &&
          !isFuture(parse(date))
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

  methods: {
    ...mapActions('context', ['setError']),
  },
};
</script>
