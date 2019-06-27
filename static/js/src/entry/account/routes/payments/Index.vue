<template>
  <div v-if="!routeIsFetching" class="has-ump-top-padding">
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
import { InvalidRouteError } from '../../errors';

export default {
  name: 'PaymentsRoute',

  components: { Appeal, CircleAppeal, MDevAppeal, Payments, Help },

  mixins: [routeMixin, userMixin],

  computed: {
    route() {
      return {
        isExact: true,
        isProtected: false,
        title: 'Donation History',
      };
    },
  },

  methods: {
    async fetchData() {
      const { never_given } = this.user;
      const meetsCriteria = !never_given;

      if (!meetsCriteria) throw new InvalidRouteError();
    },
  },
};
</script>
