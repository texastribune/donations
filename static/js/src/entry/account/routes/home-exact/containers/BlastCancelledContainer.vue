<template>
  <blast-cancelled
    v-if="isBlastCancelled"
    :last-transaction="lastTransaction"
  />
</template>

<script>
import format from 'date-fns/format';
import parse from 'date-fns/parse';

import BlastCancelled from '../components/BlastCancelled.vue';
import addNumberCommas from '../../../utils/add-number-commas';
import userMixin from '../../home/mixins/user';
import { CARD_PAYMENT_FLAG } from '../../../constants';

export default {
  name: 'BlastCancelledContainer',

  components: { BlastCancelled },

  mixins: [userMixin],

  computed: {
    isBlastCancelled() {
      // eslint-disable-next-line camelcase
      return this.user.is_former_blast_subscriber;
    },

    lastTransaction() {
      const {
        // eslint-disable-next-line camelcase
        last_blast_transaction: { amount, date, payment_type, credit_card },
      } = this.user;
      const data = {
        amount: addNumberCommas(amount),
        date: format(parse(date), 'MMMM D, YYYY'),
      };

      if (payment_type.toLowerCase() === CARD_PAYMENT_FLAG) {
        data.last4 = credit_card.last4;
      }

      return data;
    },
  },
};
</script>
