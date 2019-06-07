<template>
  <div class="has-white-bg-from-bp-l has-ump-top-padding">
    <messages :num-messages="2">
      <template v-slot="slotProps">
        <message
          heading="Welcome"
          :name="welcomeMessageKey"
          @setMessageSeen="slotProps.setMessageSeen"
        >
          <template v-slot:icon>
            <icon name="hand" :display="{ size: 's' }" />
          </template>
          <template v-slot:content>
            <p class="has-text-gray-dark t-space-heading-m t-size-s">
              <em>
                Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
                eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut
                enim ad minim veniam, quis nostrud exercitation ullamco laboris
                nisi ut aliquip ex ea commodo consequat.
              </em>
            </p>
          </template>
        </message>

        <message
          heading="Coming soon"
          :name="comingSoonMessageKey"
          @setMessageSeen="slotProps.setMessageSeen"
        >
          <template v-slot:icon>
            <icon name="clock" :display="{ size: 's' }" />
          </template>
          <template v-slot:content>
            <p class="has-text-gray-dark t-space-heading-m t-size-s">
              <em>
                Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
                eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut
                enim ad minim veniam, quis nostrud exercitation ullamco laboris
                nisi ut aliquip ex ea commodo consequat.
              </em>
            </p>
          </template>
        </message>
      </template>
    </messages>

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
import userMixin from '../home/mixins/user';
import { WELCOME_MESSAGE_KEY, COMING_SOON_MESSAGE_KEY } from '../../constants';
import ContactInfo from './containers/ContactInfoContainer.vue';
import Membership from './containers/MembershipContainer.vue';
import Expired from './containers/ExpiredContainer.vue';
import OneTime from './containers/OneTimeContainer.vue';
import NeverGiven from './containers/NeverGivenContainer.vue';
import Blast from './containers/BlastContainer.vue';
import Messages from './components/Messages.vue';
import Message from './components/Message.vue';

export default {
  name: 'Index',

  components: {
    ContactInfo,
    Membership,
    Expired,
    OneTime,
    NeverGiven,
    Blast,
    Messages,
    Message,
    Help,
  },

  mixins: [routeMixin, userMixin],

  data() {
    return {
      welcomeMessageKey: WELCOME_MESSAGE_KEY,
      comingSoonMessageKey: COMING_SOON_MESSAGE_KEY,
    };
  },
};
</script>
