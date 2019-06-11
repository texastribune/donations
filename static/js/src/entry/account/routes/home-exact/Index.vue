<template>
  <div class="has-white-bg-from-bp-l has-ump-top-padding">
    <messages />

    <h1 class="has-l-btm-marg has-ump-side-padding t-size-xl">Your Account</h1>

    <div class="c-summary-boxes has-xl-btm-marg has-ump-side-padding">
      <contact-info />
      <membership /> <expired />
      <one-time />
      <never-given />
      <blast />
    </div>

    <help home />
  </div>
</template>

<script>
import Help from '../../components/Help.vue';
import routeMixin from '../../mixins/route';
import ContactInfo from './containers/ContactInfoContainer.vue';
import Membership from './containers/MembershipContainer.vue';
import Expired from './containers/ExpiredContainer.vue';
import OneTime from './containers/OneTimeContainer.vue';
import NeverGiven from './containers/NeverGivenContainer.vue';
import Blast from './containers/BlastContainer.vue';
import Messages from './containers/MessagesContainer.vue';

export default {
  name: 'HomeExactRoute',

  components: {
    ContactInfo,
    Membership,
    Expired,
    OneTime,
    NeverGiven,
    Blast,
    Messages,
    Help,
  },

  mixins: [routeMixin],
};
</script>
