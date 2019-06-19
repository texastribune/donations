<template>
  <circle-appeal v-if="shouldShow" />
</template>

<script>
/* eslint-disable camelcase */

import CircleAppeal from '../components/CircleAppeal.vue';
import userMixin from '../mixins/user';

export default {
  name: 'CircleAppealContainer',

  components: { CircleAppeal },

  mixins: [userMixin],

  computed: {
    shouldShow() {
      const { membership_level, is_mdev } = this.user;
      const isCircle = membership_level.toLowerCase().indexOf('circle') !== -1;

      return isCircle && !is_mdev;
    },
  },
};
</script>
