<template>
  <messages-wrapper
    :is-blast="isBlast"
    :is-custom-donor="isCustomDonor"
    :is-never-given="isNeverGiven"
  />
</template>

<script>
/* eslint-disable camelcase */

import userMixin from '../../home/mixins/user';
import MessagesWrapper from '../components/MessagesWrapper.vue';

export default {
  name: 'MessagesContainer',

  components: { MessagesWrapper },

  mixins: [userMixin],

  computed: {
    isNeverGiven() {
      return this.user.never_given;
    },

    isCustomDonor() {
      return this.user.is_custom_donor;
    },

    isBlast() {
      const {
        is_former_blast_subscriber,
        is_current_blast_subscriber,
      } = this.user;

      return is_former_blast_subscriber || is_current_blast_subscriber;
    },
  },
};
</script>
