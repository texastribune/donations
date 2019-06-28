<template>
  <transition name="has-fade">
    <one-time
      v-if="shouldShow"
      :last-transaction="lastTransaction"
      :membership-expiration-date="membershipExpirationDate"
    />
  </transition>
</template>

<script>
/* eslint-disable camelcase */

import userMixin from '../../home/mixins/user';
import { CARD_PAYMENT_FLAG } from '../../../constants';

const OneTime = () =>
  import(/* webpackChunkName: "one-time-summary" */ '../components/OneTime.vue');

export default {
  name: 'OneTimeContainer',

  components: { OneTime },

  mixins: [userMixin],

  computed: {
    shouldShow() {
      const { is_one_time, is_mdev, is_expired } = this.user;

      return is_one_time && !is_mdev && !is_expired;
    },

    membershipExpirationDate() {
      return this.user.membership_expiration_date;
    },

    lastTransaction() {
      const {
        last_transaction: { amount, date, payment_type, credit_card },
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
