<template>
  <route-loader v-if="routeIsFetching">
    <template v-slot:text
      >Grabbing your account information</template
    >
  </route-loader>

  <div
    v-else
    class="has-white-bg-from-bp-l has-white-off-bg-until-bp-l has-ump-top-padding"
  >
    <messages />

    <h1 class="has-l-btm-marg has-ump-side-padding t-size-xl">Your Account</h1>

    <div class="c-summary-boxes has-xl-btm-marg has-ump-side-padding">
      <contact-info />
      <blast />
      <blast-cancelled />
      <recurring-or-circle />
      <single-or-will-expire />
      <expired />
      <never-given />
      <custom />
    </div>

    <help home />
  </div>
</template>

<script>
import routeMixin from '../../mixins/route';
import Help from '../../components/Help.vue';
import RouteLoader from '../home/components/RouteLoader.vue';
import ContactInfo from './containers/ContactInfoContainer.vue';
import RecurringOrCircle from './containers/RecurringOrCircleContainer.vue';
import Expired from './containers/ExpiredContainer.vue';
import SingleOrWillExpire from './containers/SingleOrWillExpireContainer.vue';
import NeverGiven from './containers/NeverGivenContainer.vue';
import Custom from './containers/CustomContainer.vue';
import Blast from './containers/BlastContainer.vue';
import BlastCancelled from './containers/BlastCancelledContainer.vue';
import Messages from './containers/MessagesContainer.vue';

export default {
  name: 'HomeExactRoute',

  components: {
    Messages,
    ContactInfo,
    RecurringOrCircle,
    Expired,
    SingleOrWillExpire,
    NeverGiven,
    Custom,
    Blast,
    BlastCancelled,
    Help,
    RouteLoader,
  },

  mixins: [routeMixin],

  computed: {
    route() {
      return {
        isExact: true,
        isProtected: false,
        title: 'Home',
      };
    },
  },

  methods: {
    // eslint-disable-next-line
    async fetchData() {},
  },
};
</script>
