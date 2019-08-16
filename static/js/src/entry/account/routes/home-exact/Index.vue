<template>
  <route-loader v-if="routeIsFetching">
    <template v-slot:text>
      Grabbing your account information
    </template>
  </route-loader>

  <div
    v-else
    class="has-ump-top-padding has-ump-btm-padding has-white-bg-from-bp-l has-white-off-bg-until-bp-l "
  >
    <message />

    <h1 class="has-ump-side-padding has-l-btm-marg t-size-xl">Your Account</h1>

    <div class="c-summary-boxes has-xl-btm-marg has-ump-side-padding">
      <profile-settings />
      <blast />
      <blast-cancelled />
      <recurring-or-circle />
      <single-or-will-expire />
      <expired />
      <never-given />
      <custom />
    </div>

    <div class="is-hidden-until-bp-l"><help home /></div>
  </div>
</template>

<script>
import routeMixin from '../mixin';
import Help from '../home/components/Help.vue';
import RouteLoader from '../home/components/RouteLoader.vue';
import Message from './components/Message.vue';
import ProfileSettings from './containers/ProfileSettingsContainer.vue';
import RecurringOrCircle from './containers/RecurringOrCircleContainer.vue';
import Expired from './containers/ExpiredContainer.vue';
import SingleOrWillExpire from './containers/SingleOrWillExpireContainer.vue';
import NeverGiven from './containers/NeverGivenContainer.vue';
import Custom from './containers/CustomContainer.vue';
import Blast from './containers/BlastContainer.vue';
import BlastCancelled from './containers/BlastCancelledContainer.vue';

export default {
  name: 'HomeExactRoute',

  components: {
    Message,
    ProfileSettings,
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

  data() {
    return { title: 'Home' };
  },
};
</script>
