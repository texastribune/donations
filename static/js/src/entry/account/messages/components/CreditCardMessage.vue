<template>
  <messages :num-messages="1">
    <template v-slot:messages="{ setMessageSeen }">
      <message
        heading="Coming soon"
        :name="messageKey"
        :ga-label="gaLabel"
        @setMessageSeen="setMessageSeen"
      >
        <template v-slot:icon>
          <icon name="bell" :display="{ size: 's' }" />
        </template>
        <template v-slot:content>
          <div class="has-text-gray-dark t-size-s t-links-underlined">
            <p>
              Soon, you'll be able to update your credit card, change your
              donation details and cancel your membership.
            </p>
          </div>
        </template>
      </message>
    </template>
  </messages>
</template>

<script>
import Messages from './Messages.vue';
import Message from './Message.vue';

import { READ_WRITE_CREDIT_CARD_MESSAGE_KEY } from '../../constants';

export default {
  name: 'CreditCardMessage',

  components: { Messages, Message },

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
