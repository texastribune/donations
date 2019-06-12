<template>
  <membership-detail
    :data="data"
    :is-expired="isExpired"
    :is-one-time="isOneTime"
  />
</template>

<script>
/* eslint-disable camelcase */

import isPast from 'date-fns/is_past';
import format from 'date-fns/format';
import parse from 'date-fns/parse';

import MembershipDetail from '../components/MembershipDetail.vue';
import addNumberCommas from '../../../utils/add-number-commas';
import userMixin from '../../home/mixins/user';
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

        data[0].heading = 'Last donation';
        data[0].text = `$${addNumberCommas(amount)}, ${format(
          parse(date),
          'MMMM D, YYYY'
        )}`;

        if (payment_type.toLowerCase() === CARD_PAYMENT_FLAG) {
          data[1].heading = 'Payment method';
          data[1].text = `${credit_card.brand} ending in ${credit_card.last4}`;
          data[2] = { id: 2 };
          data[2].heading = 'Status';
          data[2].text = 'Your membership is good for one year.';
        } else {
          data[1].heading = 'Status';
          data[1].text = 'Your membership is good for one year.';
        }
      } else if (recurring_donor && expired) {
        const { amount, date, payment_type, credit_card } = last_transaction;

        data[0].heading = 'Last donation';
        data[0].text = `$${addNumberCommas(amount)}, ${format(
          parse(date),
          'MMMM D, YYYY'
        )}`;

        if (payment_type.toLowerCase() === CARD_PAYMENT_FLAG) {
          data[1].heading = 'Payment method';
          data[1].text = `${credit_card.brand} ending in ${credit_card.last4}`;
          data[2] = { id: 2 };
          data[2].heading = 'Status';
          data[2].text = 'Your membership expired.';
        } else {
          data[1].heading = 'Status';
          data[1].text = 'Your membership expired.';
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
        data[0].text = `$${addNumberCommas(amount)}, ${period}`;

        if (payment_type.toLowerCase() === CARD_PAYMENT_FLAG) {
          data[1].heading = 'Payment method';
          data[1].text = `${credit_card.brand} ending in ${credit_card.last4}`;
          data[2] = { id: 2 };
          data[2].heading = 'Next payment';
          data[2].text = format(parse(date), 'MMMM D, YYYY');
        } else {
          data[1].heading = 'Next payment';
          data[1].text = format(parse(date), 'MMMM D, YYYY');
        }
      }

      return data;
    },
  },
};
</script>
