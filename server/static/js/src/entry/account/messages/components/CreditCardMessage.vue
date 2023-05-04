<template>
  <message
    heading="Coming soon"
    :name="messageKey"
    :ga-label="gaLabel"
    @setMessageSeen="$emit('setMessageSeen')"
  >
    <template #icon>
      <icon name="bell" :display="{ size: 's' }" />
    </template>
    <template #content>
      <div class="has-text-gray-dark t-size-s t-links-underlined">
        <p>
          Soon, you'll be able to update your credit card, change your donation
          details and cancel your membership.
        </p>
      </div>
    </template>
  </message>
</template>

<script>
import Message from './Message.vue';

import { READ_WRITE_CREDIT_CARD_MESSAGE_KEY } from '../../constants';

export default {
  name: 'CreditCardMessage',

  components: { Message },

  props: {
    gaLabel: {
      type: String,
      required: true,
    },
  },

  data() {
    return {
      messageKey: READ_WRITE_CREDIT_CARD_MESSAGE_KEY,
    };
  },
};
</script>
