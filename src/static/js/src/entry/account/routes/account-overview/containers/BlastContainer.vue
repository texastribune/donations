<template>
  <transition name="has-fade">
    <blast v-if="shouldShow" :next-transaction="user.nextBlastTransaction" />
  </transition>
</template>

<script>
import userMixin from '../../../store/user/mixin';

const Blast = () =>
  import(/* webpackChunkName: "summary-blast" */ '../components/Blast.vue');

export default {
  name: 'SummaryBlastContainer',

  components: { Blast },

  mixins: [userMixin],

  computed: {
    shouldShow() {
      return this.user.isCurrentBlastSubscriber;
    },
  },
};
</script>
