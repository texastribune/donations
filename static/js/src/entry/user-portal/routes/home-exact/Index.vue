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
            <icon name="camera" :display="{ size: 's' }" />
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
            <icon name="camera" :display="{ size: 's' }" />
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

    <h1 class="has-xxl-btm-marg has-ump-side-padding">Your Account</h1>

    <div class="c-summary-boxes has-xl-btm-marg has-ump-side-padding">
      <summary-box heading="contact info">
        <template v-slot:content>
          <info-list :items="data">
            <template v-slot="slotProps">
              <span
                class="has-text-gray-dark"
                :class="{ 't-wrap-break': slotProps.item.heading === 'Email' }"
              >
                {{ slotProps.item.text }}
              </span>
            </template>
          </info-list>
        </template>

        <template v-slot:links>
          <ul v-if="!pwResetSuccess && !pwResetFailure" class="c-link-list">
            <li>
              <span class="c-link-list__arrow has-text-teal">
                <strong>&rarr;</strong>
              </span>
              <span class="has-text-gray-dark">
                <button class="c-link-button" @click="resetPassword">
                  Reset your password
                </button>
              </span>
            </li>
          </ul>
          <p
            v-else-if="pwResetSuccess"
            class="t-size-xs t-space-heading-m has-text-gray"
          >
            Check your inbox for an email from The Texas Tribune with the
            subject line &quot;Reset your password.&quot;
          </p>
          <p v-else class="t-size-xs t-space-heading-m has-text-gray">
            There was an issue resetting your password. If you continue having
            trouble, email
            <a href="mailto:community@texastribune.org"
              >community@texastribune.org </a
            >.
          </p>
        </template>
      </summary-box>

      <summary-box heading="membership" :display="{ isExpired: true }">
        <template v-slot:content>
          <p class="has-text-gray-dark t-space-heading-m">
            <span class="has-text-error"
              >Your membership expired on <strong>March 29, 2019</strong>.</span
            >
            Your last donation of <strong>$35</strong> was charged on
            <strong>March 29, 2018</strong>, to your card ending in
            <strong>5555</strong>.
          </p>
        </template>
        <template v-slot:links>
          <ul class="c-link-list">
            <li class="has-xs-btm-marg">
              <span class="c-link-list__arrow has-text-teal">
                <strong>&rarr;</strong>
              </span>
              <span class="has-text-gray-dark">
                <router-link :to="{ name: 'payments' }"
                  >See your donation history</router-link
                >
              </span>
            </li>
            <li>
              <span class="c-link-list__arrow has-text-teal">
                <strong>&rarr;</strong>
              </span>
              <span class="has-text-gray-dark">
                <router-link :to="{ name: 'membership' }"
                  >More about your membership</router-link
                >
              </span>
            </li>
          </ul>
        </template>
        <template v-slot:bottom>
          <p
            class="has-text-gray-dark t-space-heading-m t-linkstyle--underlined"
          >
            To update your membership status, contact us at
            <a href="mailto:community@texastribune.org"
              >community@texastribune.org</a
            >.
          </p>
        </template>
      </summary-box>
    </div>

    <help home />
  </div>
</template>

<script>
import Help from '../../components/Help.vue';
import SummaryBox from '../../components/SummaryBox.vue';
import InfoList from '../../components/InfoList.vue';
import routeMixin from '../../mixins/route';
import userMixin from '../../mixins/user';
import routeFetchMixin from '../../mixins/route-fetch';
import Messages from './components/Messages.vue';
import Message from './components/Message.vue';
import { WELCOME_MESSAGE_KEY, COMING_SOON_MESSAGE_KEY } from '../../constants';

export default {
  name: 'Index',

  components: { Messages, Message, SummaryBox, InfoList, Help },

  mixins: [routeMixin, routeFetchMixin, userMixin],

  data() {
    return {
      data: [
        { id: 0, heading: 'Name', text: 'Andrew Gibson' },
        { id: 1, heading: 'Email', text: 'agibson@texastribune.org' },
        { id: 2, heading: 'Zip code', text: '78701' },
      ],
      welcomeMessageKey: WELCOME_MESSAGE_KEY,
      comingSoonMessageKey: COMING_SOON_MESSAGE_KEY,
      pwResetSuccess: false,
      pwResetFailure: false,
    };
  },

  methods: {
    async fetchData() {
      return '';
    },

    resetPassword() {
      this.user.resetPassword('TODO', err => {
        if (err) {
          this.pwResetFailure = true;
        } else {
          this.pwResetSuccess = true;
        }
      });
    },
  },
};
</script>
