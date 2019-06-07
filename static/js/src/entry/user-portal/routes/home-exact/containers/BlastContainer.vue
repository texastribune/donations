<template>
  <blast v-if="isBlast" :next-transaction="nextTransaction" />
</template>

<script>
import format from 'date-fns/format';
import parse from 'date-fns/parse';

import Blast from '../components/Blast.vue';
import addNumberCommas from '../../../utils/add-number-commas';
import userMixin from '../../home/mixins/user';

export default {
  name: 'BlastContainer',

  components: { Blast },

  mixins: [userMixin],

  computed: {
    isBlast() {
      // eslint-disable-next-line camelcase
      return this.user.is_blast_member;
    },

    nextTransaction() {
      const {
        next_blast_transaction: {
          amount,
          date,
          credit_card: { last4 },
        },
      } = this.user;

      return {
        amount: addNumberCommas(amount),
        date: format(parse(date), 'MMMM D, YYYY'),
        last4,
      };
    },
  },
};
</script>
