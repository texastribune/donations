<template>
  <transition name="has-fade"> <custom v-if="shouldShow" /> </transition>
</template>

<script>
/* eslint-disable camelcase */

import userMixin from '../../home/mixins/user';

const Custom = () =>
  import(/* webpackChunkName: "custom-summary" */ '../components/Custom.vue');

export default {
  name: 'CustomContainer',

  components: { Custom },

  mixins: [userMixin],

  computed: {
    shouldShow() {
      return this.user.is_custom_donor;
    },
  },
};
</script>
