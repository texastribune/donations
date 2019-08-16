<template>
  <messages :num-messages="1">
    <template v-slot="slotProps">
      <message
        heading="Welcome"
        :name="messageKey"
        :ga-close-label="ga.userPortal.labels.home"
        :display="{ onGrayMobileBg: true }"
        @setMessageSeen="slotProps.setMessageSeen"
      >
        <template v-slot:icon>
          <icon name="bell" :display="{ size: 's' }" />
        </template>
        <template v-slot:content>
          <div class="has-text-gray-dark t-size-s t-linkstyle--underlined">
            <p>
              Thanks for creating your Texas Tribune account! You can use this
              login to edit contact information, comment on texastribune.org
              stories, view donation history, download a {{ lastYear }} tax
              receipt and view Blast payment history.
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
import { READ_WRITE_WELCOME_MESSAGE_KEY } from '../../../constants';

export default {
  name: 'HomeWelcomeMessage',

  components: { Messages, Message },

  data() {
    return {
      messageKey: READ_WRITE_WELCOME_MESSAGE_KEY,
    };
  },

  computed: {
    lastYear() {
      return getYear(new Date()) - 1;
    },
  },
};
</script>
