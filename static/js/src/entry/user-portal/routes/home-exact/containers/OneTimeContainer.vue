<template>
  <one-time v-if="isOneTime" :last-transaction="lastTransaction" />
</template>

<script>
import format from 'date-fns/format';
import parse from 'date-fns/parse';

import OneTime from '../components/OneTime.vue';
import addNumberCommas from '../../../utils/add-number-commas';
import userMixin from '../../../mixins/user';

export default {
  name: 'OneTimeContainer',

  components: { OneTime },

  mixins: [userMixin],

  computed: {
    isOneTime() {
      // eslint-disable-next-line camelcase
      const { active_recurring_donor, never_given } = this.user;

      // eslint-disable-next-line camelcase
      return !active_recurring_donor && !never_given;
    },

    lastTransaction() {
      const {
        last_transaction: {
          amount,
          date,
          credit_card: { last4 },
        },
      } = this.user;

      return {
        amount: addNumberCommas(amount),
        date: format(parse(date), 'MMMM D, YYYY'),
        last4,
      };
    },
  },
};
</script>
