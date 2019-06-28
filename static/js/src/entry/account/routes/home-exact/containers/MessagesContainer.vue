<template>
  <messages-wrapper
    :is-blast="isBlast"
    :is-never-given="isNeverGiven"
    :is-m-dev="isMDev"
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
    isMDev() {
      return this.user.is_mdev;
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
