<template>
  <messages :num-messages="1">
    <template v-slot="slotProps">
      <message
        heading="Welcome"
        :name="readOnlyWelcomeMessageKey"
        :ga-close-label="ga.userPortal.labels.home"
        @setMessageSeen="slotProps.setMessageSeen"
      >
        <template v-slot:icon>
          <icon name="bell" :display="{ size: 's' }" />
        </template>
        <template v-slot:content>
          <div
            class="has-text-gray-dark t-size-s t-linkstyle--underlined t-space-heading-m"
          >
            <p class="has-b-btm-marg">
              <template v-if="isCustomDonor">
                Thanks for creating a Texas Tribune account. You can use this
                login to comment on texastribune.org stories, view your donation
                history or request a {{ lastYear }} tax receipt.
              </template>
              <template v-else-if="!isNeverGiven && isBlast">
                Thanks for creating your Texas Tribune account! You can use this
                login to comment on texastribune.org stories, view your donation
                history, download your {{ lastYear }} tax receipt and view your
                Blast payment history.
              </template>
              <template v-else-if="!isNeverGiven">
                Thanks for creating your Texas Tribune account! You can use this
                login to comment on texastribune.org stories, view your donation
                history and download a {{ lastYear }} tax receipt.
              </template>
              <template v-else-if="isBlast">
                Thanks for creating a Texas Tribune account! You can use this
                login to comment on texastribune.org stories and view your Blast
                payment history.
              </template>
              <template v-else-if="isNeverGiven">
                Thanks for creating a Texas Tribune account. You can use this
                login to comment on texastribune.org stories.
              </template>
              Later this year, you’ll also be able to update your profile
              information and newsletter preferences.
            </p>
            <p>
              Need to make a change now or have a question? Email us at
              <a
                href="mailto:community@texastribune.org"
                ga-on="click"
                :ga-event-category="ga.userPortal.category"
                :ga-event-action="ga.userPortal.actions['contact-us']"
                :ga-event-label="ga.userPortal.labels.home"
              >
                community@texastribune.org </a
              >.
            </p>
          </div>
        </template>
      </message>
    </template>
  </messages>
</template>

<script>
import getYear from 'date-fns/get_year';

import Messages from '../../../components/Messages.vue';
import Message from '../../../components/Message.vue';
import { READ_ONLY_WELCOME_MESSAGE_KEY } from '../../../constants';

export default {
  name: 'MessagesWrapper',

  components: { Messages, Message },

  props: {
    isCustomDonor: {
      type: Boolean,
      required: true,
    },

    isNeverGiven: {
      type: Boolean,
      required: true,
    },

    isBlast: {
      type: Boolean,
      required: true,
    },
  },

  data() {
    return {
      readOnlyWelcomeMessageKey: READ_ONLY_WELCOME_MESSAGE_KEY,
    };
  },

  computed: {
    lastYear() {
      return getYear(new Date()) - 1;
    },
  },
};
</script>
