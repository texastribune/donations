<template>
  <div
    v-if="route.meetsCriteria && !parentIsFetching"
    class="has-ump-top-padding"
  >
    <h1 class="has-l-btm-marg has-ump-side-padding t-size-xl">
      The Blast Newsletter: Payment History
    </h1>

    <div class="has-ump-side-padding has-xxl-btm-marg"><blast-payments /></div>

    <help blast-payments :display="{ hasTopPadding: true }" />
  </div>
</template>

<script>
/* eslint-disable camelcase */

import routeMixin from '../../mixins/route';
import userMixin from '../home/mixins/user';
import Help from '../../components/Help.vue';
import BlastPayments from './containers/BlastPaymentsContainer.vue';

export default {
  name: 'BlastPaymentsRoute',

  components: { Help, BlastPayments },

  mixins: [routeMixin, userMixin],

  props: {
    parentIsFetching: {
      type: Boolean,
      required: true,
    },
  },

  computed: {
    route() {
      const {
        is_former_blast_subscriber,
        is_current_blast_subscriber,
      } = this.user;
      const meetsCriteria =
        is_former_blast_subscriber || is_current_blast_subscriber;

      return {
        isExact: true,
        isProtected: false,
        meetsCriteria,
        title: 'The Blast Payment History',
      };
    },
  },
};
</script>
