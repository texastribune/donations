<template>
  <div v-if="route.meetsCriteria" class="has-ump-top-padding">
    <h1 class="has-l-btm-marg has-ump-side-padding t-size-xl">
      Your Donations
    </h1>

    <div class="has-ump-side-padding has-xxl-btm-marg"><payments /></div>

    <appeal />
    <circle-appeal />
    <m-dev-appeal />
    <help payments />
  </div>
</template>

<script>
/* eslint-disable camelcase */

import routeMixin from '../../mixins/route';
import userMixin from '../home/mixins/user';
import Appeal from '../home/containers/AppealContainer.vue';
import CircleAppeal from '../home/containers/CircleAppealContainer.vue';
import MDevAppeal from '../home/containers/MDevAppealContainer.vue';
import Help from '../../components/Help.vue';
import Payments from './containers/PaymentsContainer.vue';

export default {
  name: 'PaymentsRoute',

  components: { Appeal, CircleAppeal, MDevAppeal, Payments, Help },

  mixins: [routeMixin, userMixin],

  computed: {
    route() {
      const { never_given } = this.user;
      const meetsCriteria = !never_given;

      return {
        isExact: true,
        isProtected: false,
        meetsCriteria,
        title: 'Donation History',
      };
    },
  },
};
</script>
