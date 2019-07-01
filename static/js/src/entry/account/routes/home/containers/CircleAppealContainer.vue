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
      const { is_mdev, is_current_circle, is_former_circle } = this.user;

      return (is_current_circle || is_former_circle) && !is_mdev;
    },
  },
};
</script>
