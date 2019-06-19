<template>
  <appeal v-if="shouldShow" :level="user.membership_level" />
</template>

<script>
/* eslint-disable camelcase */

import Appeal from '../components/Appeal.vue';
import userMixin from '../mixins/user';

export default {
  name: 'AppealContainer',

  components: { Appeal },

  mixins: [userMixin],

  computed: {
    shouldShow() {
      const { membership_level, is_mdev } = this.user;
      const isCircle = membership_level.toLowerCase().indexOf('circle') !== -1;

      return !is_mdev && !isCircle;
    },
  },
};
</script>
