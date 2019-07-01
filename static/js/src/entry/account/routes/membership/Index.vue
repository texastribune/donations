<template>
  <div v-if="!routeIsFetching" class="has-ump-top-padding">
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
import Appeal from '../home/containers/AppealContainer.vue';
import CircleAppeal from '../home/containers/CircleAppealContainer.vue';
import Help from '../../components/Help.vue';
import { InvalidRouteError } from '../../errors';

export default {
  name: 'MembershipRoute',

  components: { Appeal, CircleAppeal, Help, MembershipDetail },

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
      const { is_mdev, never_given } = this.user;
      const meetsCriteria = !is_mdev && !never_given;

      if (!meetsCriteria) throw new InvalidRouteError();
    },
  },
};
</script>
