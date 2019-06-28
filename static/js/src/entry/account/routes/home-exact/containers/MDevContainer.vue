<template>
  <m-dev v-if="shouldShow" />
</template>

<script>
/* eslint-disable camelcase */

import MDev from '../components/MDev.vue';
import userMixin from '../../home/mixins/user';

export default {
  name: 'MDevContainer',

  components: { MDev },

  mixins: [userMixin],

  computed: {
    shouldShow() {
      return this.user.is_mdev;
    },
  },
};
</script>
