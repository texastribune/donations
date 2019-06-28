<template>
  <transition name="has-fade"> <m-dev v-if="shouldShow" /> </transition>
</template>

<script>
/* eslint-disable camelcase */

import userMixin from '../../home/mixins/user';

const MDev = () =>
  import(/* webpackChunkName: "m-dev-summary" */ '../components/MDev.vue');

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
