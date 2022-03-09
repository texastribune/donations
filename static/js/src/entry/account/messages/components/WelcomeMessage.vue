<template>
  <message
    heading="Welcome"
    :name="messageKey"
    :ga-label="gaLabel"
    :display="{ onGrayMobileBg: true }"
    @setMessageSeen="$emit('setMessageSeen')"
  >
    <template #icon>
      <icon name="bell" :display="{ size: 's' }" />
    </template>
    <template #content>
      <div class="has-text-gray-dark t-size-s t-links-underlined">
        <p>
          Thanks for creating your Texas Tribune account! You can use this login
          to edit your contact information and view your donation history and
          yearly tax receipt.
        </p>
      </div>
    </template>
  </message>
</template>

<script>
import Message from './Message.vue';

import { READ_WRITE_WELCOME_MESSAGE_KEY } from '../../constants';

export default {
  name: 'WelcomeMessage',

  components: { Message },

  props: {
    gaLabel: {
      type: String,
      required: true,
    },
  },

  data() {
    return {
      messageKey: READ_WRITE_WELCOME_MESSAGE_KEY,
    };
  },
};
</script>
