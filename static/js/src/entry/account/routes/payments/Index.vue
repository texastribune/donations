<template>
  <route-loader v-if="routeIsFetching">
    <template v-slot:text>
      Grabbing your donation history
    </template>
  </route-loader>

  <div v-else class="has-ump-top-padding">
    <credit-card-message :ga-label="ga.userPortal.labels.payments" />

    <h1 class="has-ump-side-padding has-l-btm-marg t-size-xl">
      Your Donations
    </h1>

    <div class="has-ump-side-padding has-xxl-btm-marg">
      <section class="c-detail-box has-xxl-btm-marg">
        <div class="has-xxxl-btm-marg"><detail /></div>

        <internal-nav />
      </section>

      <div class="has-xxl-btm-marg"><circle-appeal /></div>

      <div class="has-xxl-btm-marg"><custom-appeal /></div>

      <div class="c-detail-box c-detail-box--from-l">
        <link-email :ga-label="ga.userPortal.labels.payments" />
      </div>
    </div>

    <appeal />

    <help payments />
  </div>
</template>

<script>
/* eslint-disable camelcase */

import routeMixin from '../mixin';
import userMixin from '../../store/user/mixin';
import RouteLoader from '../home/components/RouteLoader.vue';
import Appeal from '../home/containers/AppealContainer.vue';
import CircleAppeal from '../home/containers/CircleAppealContainer.vue';
import CustomAppeal from '../home/containers/CustomAppealContainer.vue';
import CreditCardMessage from '../home/components/CreditCardMessage.vue';
import LinkEmail from '../home/components/LinkEmail.vue';
import Help from '../home/components/Help.vue';
import Detail from './containers/DetailContainer.vue';
import InternalNav from './components/InternalNav.vue';
import { InvalidRouteError } from '../../errors';

export default {
  name: 'PaymentsRoute',

  components: {
    LinkEmail,
    Appeal,
    CircleAppeal,
    CustomAppeal,
    Detail,
    InternalNav,
    CreditCardMessage,
    Help,
    RouteLoader,
  },

  mixins: [routeMixin, userMixin],

  data() {
    return { title: 'Donation History' };
  },

  methods: {
    async fetchData() {
      const { is_never_given } = this.user;
      const meetsCriteria = !is_never_given;

      if (!meetsCriteria) throw new InvalidRouteError();
    },
  },
};
</script>
