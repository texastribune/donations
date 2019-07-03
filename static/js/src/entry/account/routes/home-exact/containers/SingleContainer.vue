<template>
  <transition name="has-fade">
    <single
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

const Single = () =>
  import(/* webpackChunkName: "single-summary" */ '../components/Single.vue');

export default {
  name: 'SingleContainer',

  components: { Single },

  mixins: [userMixin],

  computed: {
    shouldShow() {
      const { is_single_donor, is_expired } = this.user;

      return is_single_donor && !is_expired;
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
