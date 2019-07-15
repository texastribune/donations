<template>
  <transition name="has-fade">
    <circle-z v-if="shouldShow" :next-transaction="nextTransaction" />
  </transition>
</template>

<script>
/* eslint-disable camelcase */

import userMixin from '../../home/mixins/user';
import { CARD_PAYMENT_FLAG } from '../../../constants';

const CircleZ = () =>
  import(/* webpackChunkName: "circle-summary" */ '../components/Circle.vue');

export default {
  name: 'CircleContainer',

  components: { CircleZ },

  mixins: [userMixin],

  computed: {
    shouldShow() {
      const { is_circle_donor, is_expired } = this.user;

      return is_circle_donor && !is_expired;
    },

    nextTransaction() {
      const {
        next_transaction: { amount, period, date, payment_type, credit_card },
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
