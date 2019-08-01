<template>
  <messages
    :is-blast-subscriber="isBlastSubscriber"
    :is-custom-donor="isCustomDonor"
    :is-never-given="isNeverGiven"
  />
</template>

<script>
/* eslint-disable camelcase */

import userMixin from '../../../store/user/mixin';
import Messages from '../components/Messages.vue';

export default {
  name: 'HomeMessagesContainer',

  components: { Messages },

  mixins: [userMixin],

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
