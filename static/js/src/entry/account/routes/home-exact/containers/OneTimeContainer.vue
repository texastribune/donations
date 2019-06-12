<template>
  <one-time v-if="isOneTime" :last-transaction="lastTransaction" />
</template>

<script>
/* eslint-disable camelcase */

import format from 'date-fns/format';
import parse from 'date-fns/parse';

import OneTime from '../components/OneTime.vue';
import addNumberCommas from '../../../utils/add-number-commas';
import userMixin from '../../home/mixins/user';
import { CARD_PAYMENT_FLAG } from '../../../constants';

export default {
  name: 'OneTimeContainer',

  components: { OneTime },

  mixins: [userMixin],

  computed: {
    isOneTime() {
      const { recurring_donor, never_given } = this.user;

      return !recurring_donor && !never_given;
    },

    lastTransaction() {
      const {
        last_transaction: { amount, date, payment_type, credit_card },
      } = this.user;
      const data = {
        amount: addNumberCommas(amount),
        date: format(parse(date), 'MMMM D, YYYY'),
      };

      if (payment_type && payment_type.toLowerCase() === CARD_PAYMENT_FLAG) {
        data.last4 = credit_card.last4;
      }

      return data;
    },
  },
};
</script>
