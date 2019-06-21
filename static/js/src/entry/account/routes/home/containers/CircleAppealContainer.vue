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
      const { is_mdev, is_circle } = this.user;

      return is_circle && !is_mdev;
    },
  },
};
</script>
