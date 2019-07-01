<template>
  <expired
    v-if="shouldShow"
    :last-transaction="lastTransaction"
    :is-former-circle="isFormerCircle"
    :membership-expiration-date="membershipExpirationDate"
  />
</template>

<script>
/* eslint-disable camelcase */

import Expired from '../components/Expired.vue';
import userMixin from '../../home/mixins/user';
import { CARD_PAYMENT_FLAG } from '../../../constants';

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
