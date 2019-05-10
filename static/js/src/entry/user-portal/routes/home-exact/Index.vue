<template>
  <div class="c-ump-top-route c-ump-top-route--mobile-gray-bg">
    <div class="c-temp-messages has-xxl-btm-marg">
      <message heading="Welcome" :name="welcomeMessageKey">
        <template v-slot:icon>
          <icon name="camera" size="m" />
        </template>
        <template v-slot:content>
          <p class="has-text-black-off t-space-heading-m">
            <em>
              Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
              eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut
              enim ad minim veniam, quis nostrud exercitation ullamco laboris
              nisi ut aliquip ex ea commodo consequat.
            </em>
          </p>
        </template>
      </message>
      <message heading="Coming soon" :name="comingSoonMessageKey">
        <template v-slot:icon>
          <icon name="camera" size="m" />
        </template>
        <template v-slot:content>
          <p class="has-text-black-off t-space-heading-m">
            <em>
              Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
              eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut
              enim ad minim veniam, quis nostrud exercitation ullamco laboris
              nisi ut aliquip ex ea commodo consequat.
            </em>
          </p>
        </template>
      </message>
    </div>

    <h1>Your Account</h1>

    <summary-box heading="contact info">
      <template v-slot:content>
        <info-list :items="data" />
      </template>
      <template v-slot:links>
        <ul v-if="!pwResetSuccess && !pwResetFailure">
          <li>
            &rarr;&nbsp;
            <button @click="resetPassword">Reset your password</button>
          </li>
        </ul>
        <p v-else-if="pwResetSuccess">
          Check your inbox for an email from The Texas Tribune with the subject
          line &quot;Reset your password.&quot;
        </p>
        <p v-else>
          There was an issue resetting your password. If you continue having
          trouble, contact&nbsp;
          <a href="mailto:community@texastribune.org">
            community@texastribune.org </a
          >.
        </p>
      </template>
    </summary-box>

    <summary-box heading="membership">
      <template v-slot:content>
        <info-list :items="data" />
      </template>
      <template v-slot:links>
        <ul>
          <li>
            &rarr;&nbsp;
            <router-link :to="{ name: 'payments' }"
              >See your donation history</router-link
            >
          </li>
          <li>
            &rarr;&nbsp;
            <router-link :to="{ name: 'membership' }"
              >More about your membership</router-link
            >
          </li>
        </ul>
      </template>
      <template v-slot:bottom>
        <p>
          To update your membership status, contact us at
          <a href="mailto:community@texastribune.org"
            >community@texastribune.org</a
          >.
        </p>
      </template>
    </summary-box>

    <help home />
  </div>
</template>

<script>
import Icon from '../../components/Icon.vue';
import Help from '../../components/Help.vue';
import SummaryBox from '../../components/SummaryBox.vue';
import InfoList from '../../components/InfoList.vue';
import routeMixin from '../../mixins/route';
import routeFetchMixin from '../../mixins/route-fetch';
import Message from './components/Message.vue';
import { WELCOME_MESSAGE_KEY, COMING_SOON_MESSAGE_KEY } from '../../constants';

export default {
  name: 'Index',

  components: { Message, SummaryBox, InfoList, Help, Icon },

  mixins: [routeMixin, routeFetchMixin],

  data() {
    return {
      data: [
        { id: 0, heading: 'name', text: 'Andrew Gibson' },
        { id: 1, heading: 'email', text: 'agibson@texastribune.org' },
        { id: 2, heading: 'zip', text: '78701' },
      ],
      welcomeMessageKey: WELCOME_MESSAGE_KEY,
      comingSoonMessageKey: COMING_SOON_MESSAGE_KEY,
      pwResetSuccess: false,
      pwResetFailure: false,
    };
  },

  methods: {
    async fetchData() {
      return 'foo';
    },

    resetPassword() {
      this.didResetPassword = true;
    },
  },
};
</script>
