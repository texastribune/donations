<template>
  <membership
    v-if="isRecurringAndNotExpired"
    :next-transaction="nextTransaction"
  />
</template>

<script>
import isPast from 'date-fns/is_past';
import format from 'date-fns/format';
import parse from 'date-fns/parse';

import Membership from '../components/Membership.vue';
import addNumberCommas from '../../../utils/add-number-commas';
import userMixin from '../../home/mixins/user';

export default {
  name: 'MembershipContainer',

  components: { Membership },

  mixins: [userMixin],

  computed: {
    isRecurringAndNotExpired() {
      // eslint-disable-next-line camelcase
      const { recurring_donor, membership_expiration_date } = this.user;
      const expired = isPast(parse(membership_expiration_date));

      // eslint-disable-next-line camelcase
      return recurring_donor && !expired;
    },

    nextTransaction() {
      const {
        next_transaction: {
          amount,
          period,
          date,
          credit_card: { last4 },
        },
      } = this.user;

      return {
        amount: addNumberCommas(amount),
        date: format(parse(date), 'MMMM D, YYYY'),
        last4,
        period,
      };
    },
  },
};
</script>
