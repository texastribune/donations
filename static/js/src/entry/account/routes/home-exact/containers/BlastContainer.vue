<template>
  <blast v-if="isBlast" :next-transaction="nextTransaction" />
</template>

<script>
/* eslint-disable camelcase */

import format from 'date-fns/format';
import parse from 'date-fns/parse';

import Blast from '../components/Blast.vue';
import addNumberCommas from '../../../utils/add-number-commas';
import userMixin from '../../home/mixins/user';
import { CARD_PAYMENT_FLAG } from '../../../constants';

export default {
  name: 'BlastContainer',

  components: { Blast },

  mixins: [userMixin],

  computed: {
    isBlast() {
      return this.user.is_current_blast_subscriber;
    },

    nextTransaction() {
      const {
        // eslint-disable-next-line camelcase
        next_blast_transaction: { amount, date, payment_type, credit_card },
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
