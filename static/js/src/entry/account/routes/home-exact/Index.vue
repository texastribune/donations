<template>
  <div class="has-white-bg-from-bp-l has-ump-top-padding">
    <messages />

    <h1 class="has-l-btm-marg has-ump-side-padding t-size-xl">Your Account</h1>

    <div class="c-summary-boxes has-xl-btm-marg has-ump-side-padding">
      <contact-info />
      <membership />
      <membership-expired />
      <one-time />
      <never-given />
      <m-dev />
      <blast />
      <blast-cancelled />
    </div>

    <help home />
  </div>
</template>

<script>
import routeMixin from '../../mixins/route';
import Help from '../../components/Help.vue';
import ContactInfo from './containers/ContactInfoContainer.vue';
import Membership from './containers/MembershipContainer.vue';
import MembershipExpired from './containers/MembershipExpiredContainer.vue';
import OneTime from './containers/OneTimeContainer.vue';
import NeverGiven from './containers/NeverGivenContainer.vue';
import MDev from './containers/MDevContainer.vue';
import Blast from './containers/BlastContainer.vue';
import BlastCancelled from './containers/BlastCancelledContainer.vue';
import Messages from './containers/MessagesContainer.vue';

export default {
  name: 'HomeExactRoute',

  components: {
    Messages,
    ContactInfo,
    Membership,
    MembershipExpired,
    OneTime,
    NeverGiven,
    MDev,
    Blast,
    BlastCancelled,
    Help,
  },

  mixins: [routeMixin],

  computed: {
    route() {
      return {
        isExact: true,
        isProtected: false,
        meetsCriteria: true,
        title: 'Home',
      };
    },
  },
};
</script>
