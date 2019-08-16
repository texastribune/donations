<template>
  <route-loader v-if="routeIsFetching">
    <template v-slot:text>
      Grabbing your membership information
    </template>
  </route-loader>

  <div v-else class="has-ump-top-padding">
    <credit-card-message :ga-close-label="ga.userPortal.labels.membership" />

    <h1 class="has-ump-side-padding has-xl-btm-marg t-size-xl">
      Your Membership
    </h1>

    <div class="has-ump-side-padding has-xxl-btm-marg">
      <div class="has-xxl-btm-marg">
        <expired />
        <recurring-or-circle />
        <single-or-will-expire />
      </div>

      <div class="has-xxl-btm-marg"><circle-appeal /></div>

      <div class="c-detail-box c-detail-box--from-l">
        <link-email :ga-label="ga.userPortal.labels.membership" />
      </div>
    </div>

    <appeal /> <help membership />
  </div>
</template>

<script>
/* eslint-disable camelcase */

import routeMixin from '../mixin';
import Expired from './containers/ExpiredContainer.vue';
import RecurringOrCircle from './containers/RecurringOrCircleContainer.vue';
import SingleOrWillExpire from './containers/SingleOrWillExpireContainer.vue';
import userMixin from '../../store/user/mixin';
import RouteLoader from '../home/components/RouteLoader.vue';
import LinkEmail from '../home/components/LinkEmail.vue';
import Appeal from '../home/containers/AppealContainer.vue';
import CreditCardMessage from '../home/components/CreditCardMessage.vue';
import CircleAppeal from '../home/containers/CircleAppealContainer.vue';
import Help from '../home/components/Help.vue';
import { InvalidRouteError } from '../../errors';

export default {
  name: 'MembershipRoute',

  components: {
    RouteLoader,
    Expired,
    RecurringOrCircle,
    SingleOrWillExpire,
    Appeal,
    CreditCardMessage,
    CircleAppeal,
    Help,
    LinkEmail,
  },

  mixins: [routeMixin, userMixin],

  data() {
    return { title: 'Membership' };
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
