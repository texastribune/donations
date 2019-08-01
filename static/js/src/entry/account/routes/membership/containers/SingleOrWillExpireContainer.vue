<template>
  <transition name="has-fade">
    <single-or-will-expire
      v-if="shouldShow"
      :data="data"
      :is-single-donor="isSingleDonor"
    />
  </transition>
</template>

<script>
/* eslint-disable camelcase */

import userMixin from '../../../store/user/mixin';
import formatCurrency from '../../../utils/format-currency';
import formatLongDate from '../../../utils/format-long-date';
import { CARD_PAYMENT_FLAG } from '../../../constants';

const SingleOrWillExpire = () =>
  import(/* webpackChunkName: "membership-single-or-will-expire" */ '../components/SingleOrWillExpire.vue');

export default {
  name: 'MembershipSingleOrWillExpireContainer',

  components: { SingleOrWillExpire },

  mixins: [userMixin],

  computed: {
    shouldShow() {
      const {
        is_single_donor,
        is_recurring_donor,
        is_circle_donor,
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

    data() {
      const data = [{ id: 0 }, { id: 1 }];
      const { last_transaction, membership_expiration_date } = this.user;
      const { amount, date, payment_type, credit_card } = last_transaction;

      data[0].heading = 'Donation';
      data[0].text = `${formatCurrency(amount)}, ${formatLongDate(date)}`;

      if (payment_type && payment_type.toLowerCase() === CARD_PAYMENT_FLAG) {
        data[1].heading = 'Payment method';
        data[1].text = `${credit_card.brand} ending in ${credit_card.last4}`;
        data[2] = { id: 2 };
        data[2].heading = 'Status';
        data[2].text = `Your membership is good through ${formatLongDate(
          membership_expiration_date
        )}.`;
      } else {
        data[1].heading = 'Status';
        data[1].text = `Your membership is good through ${formatLongDate(
          membership_expiration_date
        )}.`;
      }

      return data;
    },
  },
};
</script>
