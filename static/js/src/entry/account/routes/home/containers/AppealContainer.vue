<template>
  <appeal v-if="shouldShow" :level="level" :is-expired="isExpired" />
</template>

<script>
/* eslint-disable camelcase */

import isPast from 'date-fns/is_past';
import parse from 'date-fns/parse';

import Appeal from '../components/Appeal.vue';
import userMixin from '../mixins/user';

export default {
  name: 'AppealContainer',

  components: { Appeal },

  mixins: [userMixin],

  computed: {
    level() {
      return this.user.membership_level.toLowerCase();
    },

    isExpired() {
      return isPast(parse(this.user.membership_expiration_date));
    },

    shouldShow() {
      const { membership_level, is_mdev } = this.user;
      const isCircle = membership_level.toLowerCase().indexOf('circle') !== -1;

      return !is_mdev && !isCircle;
    },
  },
};
</script>
