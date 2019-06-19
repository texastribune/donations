<template>
  <m-dev-appeal v-if="shouldShow" />
</template>

<script>
/* eslint-disable camelcase */

import MDevAppeal from '../components/MDevAppeal.vue';
import userMixin from '../mixins/user';

export default {
  name: 'MDevAppealContainer',

  components: { MDevAppeal },

  mixins: [userMixin],

  computed: {
    shouldShow() {
      return this.user.is_mdev;
    },
  },
};
</script>
