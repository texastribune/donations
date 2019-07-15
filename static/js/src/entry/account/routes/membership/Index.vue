<template>
  <route-loader v-if="routeIsFetching">
    <template v-slot:text
      >Grabbing your membership information</template
    >
  </route-loader>

  <div v-else class="has-ump-top-padding">
    <h1 class="has-xl-btm-marg has-ump-side-padding t-size-xl">
      Your Membership
    </h1>

    <div class="has-ump-side-padding has-xl-btm-marg">
      <membership-detail />
    </div>

    <appeal />
    <circle-appeal />
    <help membership />
  </div>
</template>

<script>
/* eslint-disable camelcase */

import MembershipDetail from './containers/MembershipDetailContainer.vue';
import routeMixin from '../../mixins/route';
import userMixin from '../home/mixins/user';
import RouteLoader from '../home/components/RouteLoader.vue';
import Appeal from '../home/containers/AppealContainer.vue';
import CircleAppeal from '../home/containers/CircleAppealContainer.vue';
import Help from '../../components/Help.vue';
import { InvalidRouteError } from '../../errors';

export default {
  name: 'MembershipRoute',

  components: { Appeal, CircleAppeal, Help, MembershipDetail, RouteLoader },

  mixins: [routeMixin, userMixin],

  computed: {
    route() {
      return {
        isExact: true,
        isProtected: false,
        title: 'Membership',
      };
    },
  },

  methods: {
    async fetchData() {
      const {
        is_recurring_donor,
        is_single_donor,
        is_circle_donor,
      } = this.user;

      const meetsCriteria =
        is_recurring_donor || is_single_donor || is_circle_donor;

      if (!meetsCriteria) throw new InvalidRouteError();
    },
  },
};
</script>
