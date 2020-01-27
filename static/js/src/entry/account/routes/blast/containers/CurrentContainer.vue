<template>
  <transition name="has-fade">
    <current v-if="shouldShow" :next-transaction="user.nextBlastTransaction" />
  </transition>
</template>

<script>
import userMixin from '../../../store/user/mixin';

const Current = () =>
  import(/* webpackChunkName: "blast-current" */ '../components/Current.vue');

export default {
  name: 'BlastCurrentContainer',

  components: { Current },

  mixins: [userMixin],

  computed: {
    shouldShow() {
      return this.user.isCurrentBlastSubscriber;
    },
  },
};
</script>
