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
      const data = [
        { id: 0, heading: 'Donation', text: '' },
        { id: 1, heading: 'Payment method', text: '' },
        { id: 2 },
      ];
      const {
        recurring_donor,
        membership_expiration_date,
        next_transaction,
        last_transaction,
      } = this.user;
      const expired = isPast(parse(membership_expiration_date));

      if (!recurring_donor) {
        const {
          amount,
          date,
          credit_card: { last4, brand },
        } = last_transaction;

        data[0].text = `$${addNumberCommas(amount)}, ${format(
          parse(date),
          'MMMM D, YYYY'
        )}`;
        data[1].text = `${brand} ending in ${last4}`;
        data[2].heading = 'Status';
        data[2].text = `Your membership is good through ${format(
          parse(membership_expiration_date),
          'MMMM D, YYYY'
        )}.`;
      } else if (recurring_donor && expired) {
        const {
          amount,
          date,
          credit_card: { last4, brand },
        } = last_transaction;

        data[0].text = `$${addNumberCommas(amount)}, ${format(
          parse(date),
          'MMMM D, YYYY'
        )}`;
        data[1].text = `${brand} ending in ${last4}`;
        data[2].heading = 'Status';
        data[2].text = 'Your membership expired.';
      } else if (recurring_donor && !expired) {
        const {
          amount,
          date,
          period,
          credit_card: { last4, brand },
        } = next_transaction;

        data[0].text = `$${addNumberCommas(amount)}, ${period}`;
        data[1].text = `${brand} ending in ${last4}`;
        data[2].heading = 'Next payment';
        data[2].text = format(parse(date), 'MMMM D, YYYY');
      }

      return data;
    },
  },
};
</script>
