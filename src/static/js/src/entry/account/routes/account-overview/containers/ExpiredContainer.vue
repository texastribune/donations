<template>
  <transition name="has-fade">
    <expired
      v-if="shouldShow"
      :last-transaction="user.lastTransaction"
      :membership-expiration-date="user.membershipExpirationDate"
    />
  </transition>
</template>

<script>
import userMixin from '../../../store/user/mixin';

const Expired = () =>
  import(/* webpackChunkName: "summary-expired" */ '../components/Expired.vue');

export default {
  name: 'SummaryExpiredContainer',

  components: { Expired },

  mixins: [userMixin],

  computed: {
    shouldShow() {
      const { hasGivenNotCustom, isExpired } = this.user;

      return hasGivenNotCustom && isExpired;
    },
  },
};
</script>
