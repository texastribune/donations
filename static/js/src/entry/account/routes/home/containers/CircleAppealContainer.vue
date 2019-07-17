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
      return this.user.is_circle_donor;
    },
  },
};
</script>
