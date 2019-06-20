<template>
  <one-time
    v-if="shouldShow"
    :last-transaction="lastTransaction"
    :membership-expiration-date="membershipExpirationDate"
  />
</template>

<script>
/* eslint-disable camelcase */

import OneTime from '../components/OneTime.vue';
import userMixin from '../../home/mixins/user';
import { CARD_PAYMENT_FLAG } from '../../../constants';

export default {
  name: 'OneTimeContainer',

  components: { OneTime },

  mixins: [userMixin],

  computed: {
    shouldShow() {
      const { recurring_donor, never_given, is_mdev } = this.user;

      return !recurring_donor && !never_given && !is_mdev;
    },

    membershipExpirationDate() {
      return this.user.membership_expiration_date;
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
