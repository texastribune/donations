<template>
  <blast-detail :data="data" />
</template>

<script>
/* eslint-disable camelcase */

import format from 'date-fns/format';
import parse from 'date-fns/parse';

import BlastDetail from '../components/BlastDetail.vue';
import userMixin from '../../home/mixins/user';

export default {
  name: 'BlastDetailContainer',

  components: { BlastDetail },

  mixins: [userMixin],

  computed: {
    data() {
      const data = [
        { id: 0, heading: 'Subscription', text: '' },
        { id: 1, heading: 'Payment method', text: '' },
        { id: 2, heading: 'Next payment', text: '' },
      ];
      const {
        next_blast_transaction: {
          amount,
          period,
          date,
          credit_card: { last4, brand },
        },
      } = this.user;

      data[0].text = `$${amount}, ${period}`;
      data[1].text = `${brand} ending in ${last4}`;
      data[2].text = format(parse(date), 'MMMM D, YYYY');

      return data;
    },
  },
};
</script>
