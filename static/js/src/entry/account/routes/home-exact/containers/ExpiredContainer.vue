<template>
  <transition name="has-fade">
    <expired
      v-if="shouldShow"
      :is-circle-donor="isCircleDonor"
      :last-transaction="lastTransaction"
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
      const {
        is_recurring_donor,
        is_single_donor,
        is_circle_donor,
        is_expired,
      } = this.user;

      return (
        (is_recurring_donor || is_single_donor || is_circle_donor) && is_expired
      );
    },

    membershipExpirationDate() {
      return this.user.membership_expiration_date;
    },

    isCircleDonor() {
      return this.user.is_circle_donor;
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
