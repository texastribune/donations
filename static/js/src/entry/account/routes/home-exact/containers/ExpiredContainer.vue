<template>
  <transition name="has-fade">
    <expired
      v-if="shouldShow"
      :last-transaction="lastTransaction"
      :is-former-circle="isFormerCircle"
      :membership-expiration-date="membershipExpirationDate"
    />
  </transition>
</template>

<script>
/* eslint-disable camelcase */

import userMixin from '../../home/mixins/user';
import { CARD_PAYMENT_FLAG } from '../../../constants';

const Expired = () =>
  import(/* webpackChunkName: "expired-summary" */ '../components/Expired.vue');

export default {
  name: 'ExpiredContainer',

  components: { Expired },

  mixins: [userMixin],

  computed: {
    shouldShow() {
      const { never_given, is_expired, is_mdev } = this.user;

      return !never_given && is_expired && !is_mdev;
    },

    membershipExpirationDate() {
      return this.user.membership_expiration_date;
    },

    isFormerCircle() {
      return this.user.is_former_circle;
    },

    lastTransaction() {
      const {
        last_transaction: { amount, date, payment_type, credit_card },
      } = this.user;

      const data = {
        amount,
        date,
      };

      if (payment_type && payment_type.toLowerCase() === CARD_PAYMENT_FLAG) {
        data.last4 = credit_card.last4;
      }

      return data;
    },
  },
};
</script>
