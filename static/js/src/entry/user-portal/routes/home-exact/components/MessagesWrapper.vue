<template>
  <messages :num-messages="1">
    <template v-slot="slotProps">
      <message
        heading="Welcome"
        :name="readOnlyWelcomeMessageKey"
        @setMessageSeen="slotProps.setMessageSeen"
      >
        <template v-slot:icon>
          <icon name="bell" :display="{ size: 's' }" />
        </template>
        <template v-slot:content>
          <p class="has-text-gray-dark t-space-heading-m t-size-s">
            <em>
              <template v-if="isRecurring && isBlast">
                Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
                eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut
                enim ad minim veniam, quis nostrud exercitation ullamco laboris
                nisi ut aliquip ex ea commodo consequat.
              </template>
              <template v-else-if="isRecurring">
                Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
                eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut
                enim ad minim veniam, quis nostrud exercitation ullamco laboris
                nisi ut aliquip ex ea commodo consequat.
              </template>
              <template v-else-if="isBlast">
                Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
                eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut
                enim ad minim veniam, quis nostrud exercitation ullamco laboris
                nisi ut aliquip ex ea commodo consequat.
              </template>
              <template v-else-if="isNeverGiven">
                Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
                eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut
                enim ad minim veniam, quis nostrud exercitation ullamco laboris
                nisi ut aliquip ex ea commodo consequat.
              </template>
            </em>
          </p>
        </template>
      </message>
    </template>
  </messages>
</template>

<script>
import Messages from '../../../components/Messages.vue';
import Message from '../../../components/Message.vue';
import { READ_ONLY_WELCOME_MESSAGE_KEY } from '../../../constants';

export default {
  name: 'MessagesWrapper',

  components: { Messages, Message },

  props: {
    isRecurring: {
      type: Boolean,
      required: true,
    },

    isBlast: {
      type: Boolean,
      required: true,
    },

    isNeverGiven: {
      type: Boolean,
      required: true,
    },
  },

  data() {
    return {
      readOnlyWelcomeMessageKey: READ_ONLY_WELCOME_MESSAGE_KEY,
    };
  },
};
</script>
