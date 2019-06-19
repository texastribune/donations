<template>
  <blast-detail :data="data" :is-cancelled="isCancelled" />
</template>

<script>
/* eslint-disable camelcase */

import BlastDetail from '../components/BlastDetail.vue';
import userMixin from '../../home/mixins/user';
import { CARD_PAYMENT_FLAG } from '../../../constants';

export default {
  name: 'BlastDetailContainer',

  components: { BlastDetail },

  mixins: [userMixin],

  computed: {
    isCancelled() {
      return this.user.is_former_blast_subscriber;
    },

    data() {
      const data = [{ id: 0 }, { id: 1 }];
      const {
        next_blast_transaction,
        last_blast_transaction,
        is_former_blast_subscriber,
        is_current_blast_subscriber,
      } = this.user;

      if (is_current_blast_subscriber) {
        const {
          amount,
          period,
          date,
          payment_type,
          credit_card,
        } = next_blast_transaction;

        data[0].heading = 'Subscription';
        data[0].text = `${amount}|${period}`;

        if (payment_type && payment_type.toLowerCase() === CARD_PAYMENT_FLAG) {
          data[1].heading = 'Payment method';
          data[1].text = `${credit_card.brand} ending in ${credit_card.last4}`;
          data[2] = { id: 2 };
          data[2].heading = 'Next payment';
          data[2].text = date;
        } else {
          data[1].heading = 'Next payment';
          data[1].text = date;
        }
      } else if (is_former_blast_subscriber) {
        const {
          amount,
          period,
          payment_type,
          credit_card,
        } = last_blast_transaction;

        data[0].heading = 'Past subscription';
        data[0].text = `${amount}|${period}`;

        if (payment_type && payment_type.toLowerCase() === CARD_PAYMENT_FLAG) {
          data[1].heading = 'Payment method';
          data[1].text = `${credit_card.brand} ending in ${credit_card.last4}`;
          data[2] = { id: 2 };
          data[2].heading = 'Status';
          data[2].text = 'Your subscription was cancelled.';
        } else {
          data[1].heading = 'Status';
          data[1].text = 'Your subscription was cancelled.';
        }
      }

      return data;
    },
  },
};
</script>
