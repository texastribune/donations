<template>
  <transition name="has-fade">
    <single-or-will-expire
      v-if="shouldShow"
      :last-transaction="lastTransaction"
      :is-single-donor="isSingleDonor"
      :membership-expiration-date="membershipExpirationDate"
    />
  </transition>
</template>

<script>
/* eslint-disable camelcase */

import userMixin from '../../../store/user/mixin';
import { CARD_PAYMENT_FLAG } from '../../../constants';

const SingleOrWillExpire = () =>
  import(/* webpackChunkName: "summary-single-or-will-expire" */ '../components/SingleOrWillExpire.vue');

export default {
  name: 'SummarySingleOrWillExpireContainer',

  components: { SingleOrWillExpire },

  mixins: [userMixin],

  computed: {
    shouldShow() {
      const {
        is_single_donor,
        is_circle_donor,
        is_recurring_donor,
        will_expire,
        is_expired,
      } = this.user;

      return (
        (is_single_donor && !is_expired) ||
        ((is_recurring_donor || is_circle_donor) && will_expire)
      );
    },

    isSingleDonor() {
      return this.user.is_single_donor;
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
