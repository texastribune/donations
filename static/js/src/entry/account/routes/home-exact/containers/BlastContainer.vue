<template>
  <blast v-if="shouldShow" :next-transaction="nextTransaction" />
</template>

<script>
/* eslint-disable camelcase */

import Blast from '../components/Blast.vue';
import userMixin from '../../home/mixins/user';
import { CARD_PAYMENT_FLAG } from '../../../constants';

export default {
  name: 'BlastContainer',

  components: { Blast },

  mixins: [userMixin],

  computed: {
    shouldShow() {
      return this.user.is_current_blast_subscriber;
    },

    nextTransaction() {
      const {
        next_blast_transaction: {
          amount,
          date,
          payment_type,
          period,
          credit_card,
        },
      } = this.user;

      const data = {
        amount,
        date,
        period,
      };

      if (payment_type && payment_type.toLowerCase() === CARD_PAYMENT_FLAG) {
        data.last4 = credit_card.last4;
      }

      return data;
    },
  },
};
</script>
