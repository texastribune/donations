<template>
  <payments
    :data="data"
    :is-expired="isExpired"
    :is-one-time="isOneTime"
    :is-former-circle="isFormerCircle"
    :is-m-dev="isMDev"
    :total-gifts-last-year="totalGiftsLastYear"
    :greeting="greeting"
  />
</template>

<script>
/* eslint-disable camelcase */

import parse from 'date-fns/parse';
import isFuture from 'date-fns/is_future';

import Payments from '../components/Payments.vue';
import userMixin from '../../home/mixins/user';
import { BLAST_PAYMENT_FLAG, CARD_PAYMENT_FLAG } from '../../../constants';

export default {
  name: 'PaymentsContainer',

  components: { Payments },

  mixins: [userMixin],

  computed: {
    isOneTime() {
      return this.user.is_one_time;
    },

    isExpired() {
      return this.user.is_expired;
    },

    isMDev() {
      return this.user.is_mdev;
    },

    isFormerCircle() {
      return this.user.is_former_circle;
    },

    totalGiftsLastYear() {
      return this.user.total_gifts_last_year;
    },

    greeting() {
      return this.user.greeting;
    },

    data() {
      const { transactions } = this.user;
      const relevantTransactions = transactions.filter(
        ({ type, date }) =>
          type.toLowerCase() !== BLAST_PAYMENT_FLAG && !isFuture(parse(date))
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
