<template>
  <transition name="has-fade">
    <recurring-or-circle v-if="shouldShow" :data="data" />
  </transition>
</template>

<script>
/* eslint-disable camelcase */

import userMixin from '../../../store/user/mixin';
import formatCurrency from '../../../utils/format-currency';
import formatLongDate from '../../../utils/format-long-date';
import { CARD_PAYMENT_FLAG } from '../../../constants';

const RecurringOrCircle = () =>
  import(/* webpackChunkName: "membership-recurring-or-circle" */ '../components/RecurringOrCircle.vue');

export default {
  name: 'MembershipRecurringOrCircleContainer',

  components: { RecurringOrCircle },

  mixins: [userMixin],

  computed: {
    shouldShow() {
      const {
        is_circle_donor,
        is_recurring_donor,
        will_expire,
        is_expired,
      } = this.user;

      return (
        (is_circle_donor || is_recurring_donor) && !is_expired && !will_expire
      );
    },

    data() {
      const data = [{ id: 0 }, { id: 1 }];
      const { next_transaction } = this.user;
      const {
        amount,
        date,
        period,
        payment_type,
        credit_card,
      } = next_transaction;

      data[0].heading = 'Donation';
      data[0].text = `${formatCurrency(amount)}, ${period}`;

      if (payment_type && payment_type.toLowerCase() === CARD_PAYMENT_FLAG) {
        data[1].heading = 'Payment method';
        data[1].text = `${credit_card.brand} ending in ${credit_card.last4}`;
        data[2] = { id: 2 };
        data[2].heading = 'Next payment';
        data[2].text = formatLongDate(date);
      } else {
        data[1].heading = 'Next payment';
        data[1].text = formatLongDate(date);
      }

      return data;
    },
  },
};
</script>
