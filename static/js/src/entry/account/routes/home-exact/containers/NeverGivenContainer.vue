<template>
  <transition name="has-fade"> <never-given v-if="shouldShow" /> </transition>
</template>

<script>
import userMixin from '../../home/mixins/user';

const NeverGiven = () =>
  import(/* webpackChunkName: "never-given-summary" */ '../components/NeverGiven.vue');

export default {
  name: 'NeverGivenContainer',

  components: { NeverGiven },

  mixins: [userMixin],

  computed: {
    shouldShow() {
      return this.user.never_given;
    },
  },
};
</script>
