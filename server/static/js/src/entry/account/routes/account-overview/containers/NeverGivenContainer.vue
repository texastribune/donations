<template>
  <transition name="has-fade"> <never-given v-if="shouldShow" /> </transition>
</template>

<script>
import userMixin from '../../../store/user/mixin';

const NeverGiven = () =>
  import(/* webpackChunkName: "summary-never-given" */ '../components/NeverGiven.vue');

export default {
  name: 'SummaryNeverGivenContainer',

  components: { NeverGiven },

  mixins: [userMixin],

  computed: {
    shouldShow() {
      return this.user.isNeverGiven;
    },
  },
};
</script>
