<template>
  <transition name="has-fade">
    <former v-if="shouldShow" :last-transaction="user.lastBlastTransaction" />
  </transition>
</template>

<script>
import userMixin from '../../../store/user/mixin';

const Former = () =>
  import(/* webpackChunkName: "blast-former" */ '../components/Former.vue');

export default {
  name: 'BlastFormerContainer',

  components: { Former },

  mixins: [userMixin],

  computed: {
    shouldShow() {
      return this.user.isFormerBlastSubscriber;
    },
  },
};
</script>
