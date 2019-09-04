<template>
  <transition name="has-fade">
    <blast v-if="shouldShow" :next-transaction="nextTransaction" />
  </transition>
</template>

<script>
/* eslint-disable camelcase */

import userMixin from '../../../store/user/mixin';
import { CARD_PAYMENT_FLAG } from '../../../constants';

const Blast = () =>
  import(/* webpackChunkName: "summary-blast" */ '../components/Blast.vue');

export default {
  name: 'SummaryBlastContainer',

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
