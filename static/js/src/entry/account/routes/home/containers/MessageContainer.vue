<template>
  <message
    :is-blast-subscriber="isBlastSubscriber"
    :is-custom-donor="isCustomDonor"
    :is-never-given="isNeverGiven"
    :ga-close-label="gaCloseLabel"
    :display="display"
  />
</template>

<script>
/* eslint-disable camelcase */

import userMixin from '../../../store/user/mixin';
import Message from '../components/Message.vue';

export default {
  name: 'HomeWelcomeMessageContainer',

  components: { Message },

  mixins: [userMixin],

  props: {
    gaCloseLabel: {
      type: String,
      required: true,
    },

    display: {
      type: Object,
      default: () => ({}),
    },
  },

  computed: {
    isNeverGiven() {
      return this.user.never_given;
    },

    isCustomDonor() {
      return this.user.is_custom_donor;
    },

    isBlastSubscriber() {
      return this.user.is_blast_subscriber;
    },
  },
};
</script>
