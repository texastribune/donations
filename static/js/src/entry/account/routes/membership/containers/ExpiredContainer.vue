<template>
  <transition name="has-fade">
    <expired
      v-if="shouldShow"
      :data="data"
      :is-single-donor="isSingleDonor"
      :is-circle-donor="isCircleDonor"
    />
  </transition>
</template>

<script>
/* eslint-disable camelcase */

import userMixin from '../../../store/user/mixin';
import formatCurrency from '../../../utils/format-currency';
import formatLongDate from '../../../utils/format-long-date';
import { CARD_PAYMENT_FLAG } from '../../../constants';

const Expired = () =>
  import(/* webpackChunkName: "membership-expired" */ '../components/Expired.vue');

export default {
  name: 'MembershipExpiredContainer',

  components: { Expired },

  mixins: [userMixin],

  computed: {
    shouldShow() {
      return this.user.is_expired;
    },

    isSingleDonor() {
      return this.user.is_single_donor;
    },

    isCircleDonor() {
      return this.user.is_circle_donor;
    },

    data() {
      const data = [{ id: 0 }, { id: 1 }];
      const { last_transaction, membership_expiration_date } = this.user;
      const { amount, date, payment_type, credit_card } = last_transaction;

      data[0].heading = 'Last donation';
      data[0].text = `${formatCurrency(amount)}, ${formatLongDate(date)}`;

      if (payment_type && payment_type.toLowerCase() === CARD_PAYMENT_FLAG) {
        data[1].heading = 'Payment method';
        data[1].text = `${credit_card.brand} ending in ${credit_card.last4}`;
        data[2] = { id: 2 };
        data[2].heading = 'Status';
        data[2].text = `Your membership expired on ${formatLongDate(
          membership_expiration_date
        )}.`;
      } else {
        data[1].heading = 'Status';
        data[1].text = `Your membership expired on ${formatLongDate(
          membership_expiration_date
        )}.`;
      }

      return data;
    },
  },
};
</script>
