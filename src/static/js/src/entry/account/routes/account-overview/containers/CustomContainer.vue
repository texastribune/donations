<template>
  <transition name="has-fade"> <custom v-if="shouldShow" /> </transition>
</template>

<script>
import userMixin from '../../../store/user/mixin';

const Custom = () =>
  import(/* webpackChunkName: "summary-custom" */ '../components/Custom.vue');

export default {
  name: 'SummaryCustomContainer',

  components: { Custom },

  mixins: [userMixin],

  computed: {
    shouldShow() {
      return this.user.isCustomDonor;
    },
  },
};
</script>
