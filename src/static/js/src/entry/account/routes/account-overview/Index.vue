<template>
  <div
    class="
      has-ump-top-padding
      has-ump-btm-padding
      has-white-bg-from-bp-l
      has-white-off-bg-until-bp-l
    "
  >
    <messages :num-messages="1">
      <template #messages="{ setMessageSeen }">
        <welcome-message
          :ga-label="ga.userPortal.labels.home"
          @setMessageSeen="setMessageSeen"
        />
      </template>
    </messages>

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

    <div class="is-hidden-until-bp-l">
      <contact-us :ga-label="ga.userPortal.labels.home">
        <template #text>
          Have questions about your account? Or feedback about this website?
          Email
        </template>
      </contact-us>
    </div>
  </div>
</template>

<script>
import routeMixin from '../mixin';

import ProfileSettings from './containers/ProfileSettingsContainer.vue';
import RecurringOrCircle from './containers/RecurringOrCircleContainer.vue';
import Expired from './containers/ExpiredContainer.vue';
import SingleOrWillExpire from './containers/SingleOrWillExpireContainer.vue';
import NeverGiven from './containers/NeverGivenContainer.vue';
import Custom from './containers/CustomContainer.vue';
import Blast from './containers/BlastContainer.vue';
import BlastCancelled from './containers/BlastCancelledContainer.vue';

import Messages from '../../messages/components/Messages.vue';
import WelcomeMessage from '../../messages/components/WelcomeMessage.vue';
import ContactUs from '../../components/ContactUs.vue';

export default {
  name: 'AccountOverviewRoute',

  components: {
    Messages,
    WelcomeMessage,
    ProfileSettings,
    RecurringOrCircle,
    Expired,
    SingleOrWillExpire,
    NeverGiven,
    Custom,
    Blast,
    BlastCancelled,
    ContactUs,
  },

  mixins: [routeMixin],
};
</script>
