<template>
  <messages :num-messages="1">
    <template v-slot="slotProps">
      <message
        heading="Coming soon"
        :name="messageKey"
        :ga-close-label="gaCloseLabel"
        @setMessageSeen="slotProps.setMessageSeen"
      >
        <template v-slot:icon>
          <icon name="bell" :display="{ size: 's' }" />
        </template>
        <template v-slot:content>
          <div class="has-text-gray-dark t-size-s t-linkstyle--underlined">
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
import Messages from '../../../components/Messages.vue';
import Message from '../../../components/Message.vue';
import { READ_WRITE_CREDIT_CARD_MESSAGE_KEY } from '../../../constants';

export default {
  name: 'CreditCardMessage',

  components: { Messages, Message },

  props: {
    gaCloseLabel: {
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
