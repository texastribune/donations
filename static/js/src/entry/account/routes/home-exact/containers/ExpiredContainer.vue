<template>
  <expired
    v-if="shouldShow"
    :last-transaction="lastTransaction"
    :is-circle="isCircle"
    :membership-expiration-date="membershipExpirationDate"
  />
</template>

<script>
/* eslint-disable camelcase */

import isPast from 'date-fns/is_past';
import parse from 'date-fns/parse';

import Expired from '../components/Expired.vue';
import userMixin from '../../home/mixins/user';
import { CARD_PAYMENT_FLAG } from '../../../constants';

export default {
  name: 'ExpiredContainer',

  components: { Expired },

  mixins: [userMixin],

  computed: {
    shouldShow() {
      const { never_given, membership_expiration_date, is_mdev } = this.user;
      const isExpired = isPast(parse(membership_expiration_date));

      return !never_given && isExpired && !is_mdev;
    },

    membershipExpirationDate() {
      return this.user.membership_expiration_date;
    },

    isCircle() {
      return this.user.membership_level.toLowerCase().indexOf('circle') !== -1;
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
