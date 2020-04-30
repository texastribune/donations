<template>
  <transition name="has-fade">
    <blast-cancelled
      v-if="shouldShow"
      :last-transaction="user.lastBlastTransaction"
    />
  </transition>
</template>

<script>
import userMixin from '../../../store/user/mixin';

const BlastCancelled = () =>
  import(/* webpackChunkName: "summary-blast-cancelled" */ '../components/BlastCancelled.vue');

export default {
  name: 'SummaryBlastCancelledContainer',

  components: { BlastCancelled },

  mixins: [userMixin],

  computed: {
    shouldShow() {
      return this.user.isFormerBlastSubscriber;
    },
  },
};
</script>
