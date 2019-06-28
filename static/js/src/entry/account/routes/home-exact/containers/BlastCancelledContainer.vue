<template>
  <transition name="has-fade">
    <blast-cancelled v-if="shouldShow" :last-transaction="lastTransaction" />
  </transition>
</template>

<script>
/* eslint-disable camelcase */

import userMixin from '../../home/mixins/user';
import { CARD_PAYMENT_FLAG } from '../../../constants';

const BlastCancelled = () =>
  import(/* webpackChunkName: "blast-cancelled-summary" */ '../components/BlastCancelled.vue');

export default {
  name: 'BlastCancelledContainer',

  components: { BlastCancelled },

  mixins: [userMixin],

  computed: {
    shouldShow() {
      return this.user.is_former_blast_subscriber;
    },

    lastTransaction() {
      const {
        last_blast_transaction: { amount, date, payment_type, credit_card },
      } = this.user;

      const data = { amount, date };

      if (payment_type && payment_type.toLowerCase() === CARD_PAYMENT_FLAG) {
        data.last4 = credit_card.last4;
      }

      return data;
    },
  },
};
</script>
