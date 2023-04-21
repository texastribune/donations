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
  import(/* webpackChunkName: "membership-expired" */ '../components/Expired.vue');

export default {
  name: 'MembershipExpiredContainer',

  components: { Expired },

  mixins: [userMixin],

  computed: {
    shouldShow() {
      return this.user.isExpired;
    },
  },
};
</script>
