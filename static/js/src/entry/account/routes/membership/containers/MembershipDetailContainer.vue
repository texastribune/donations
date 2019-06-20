<template>
  <membership-detail
    :data="data"
    :is-expired="isExpired"
    :is-one-time="isOneTime"
    :is-circle="isCircle"
  />
</template>

<script>
/* eslint-disable camelcase */

import isPast from 'date-fns/is_past';
import parse from 'date-fns/parse';

import MembershipDetail from '../components/MembershipDetail.vue';
import userMixin from '../../home/mixins/user';
import formatCurrency from '../../../utils/format-currency';
import formatLongDate from '../../../utils/format-long-date';
import { CARD_PAYMENT_FLAG } from '../../../constants';

export default {
  name: 'MembershipDetailContainer',

  components: { MembershipDetail },

  mixins: [userMixin],

  computed: {
    isOneTime() {
      return !this.user.recurring_donor;
    },

    isExpired() {
      return isPast(parse(this.user.membership_expiration_date));
    },

    isCircle() {
      return this.user.membership_level.toLowerCase().indexOf('circle') !== -1;
    },

    data() {
      const data = [{ id: 0 }, { id: 1 }];
      const {
        recurring_donor,
        membership_expiration_date,
        next_transaction,
        last_transaction,
      } = this.user;
      const expired = isPast(parse(membership_expiration_date));

      if (!recurring_donor) {
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
      } else if (recurring_donor && expired) {
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
      } else if (recurring_donor && !expired) {
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
      }

      return data;
    },
  },
};
</script>
