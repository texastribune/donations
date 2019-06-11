<template>
  <messages-wrapper
    :is-recurring="isRecurring"
    :is-blast="isBlast"
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
    isRecurring() {
      return this.user.recurring_donor;
    },

    isBlast() {
      const {
        is_former_blast_subscriber,
        is_current_blast_subscriber,
      } = this.user;

      return is_former_blast_subscriber || is_current_blast_subscriber;
    },

    isNeverGiven() {
      return this.user.never_given;
    },
  },
};
</script>
