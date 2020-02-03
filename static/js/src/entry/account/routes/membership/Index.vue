<template>
  <route-loader v-if="routeIsFetching">
    <template v-slot:text>
      Grabbing your membership information
    </template>
  </route-loader>

  <div v-else class="has-ump-top-padding">
    <credit-card-message :ga-label="ga.userPortal.labels.membership" />

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

    <appeal />

    <help membership />
  </div>
</template>

<script>
import Help from '../../components/Help.vue';
import { InvalidRouteError } from '../../errors';
import userMixin from '../../store/user/mixin';
import LinkEmail from '../../link-email/components/LinkEmail.vue';
import CircleAppeal from '../../appeals/components/CircleAppeal.vue';
import Appeal from '../../appeals/containers/AppealContainer.vue';
import CreditCardMessage from '../../messages/components/CreditCardMessage.vue';
import routeMixin from '../mixin';
import RouteLoader from '../home/components/RouteLoader.vue';
import Expired from './containers/ExpiredContainer.vue';
import RecurringOrCircle from './containers/RecurringOrCircleContainer.vue';
import SingleOrWillExpire from './containers/SingleOrWillExpireContainer.vue';

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
      const { hasGivenNotCustom } = this.user;
      const meetsCriteria = hasGivenNotCustom;

      if (!meetsCriteria) throw new InvalidRouteError();
    },
  },
};
</script>
