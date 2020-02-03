<template>
  <appeal
    v-if="shouldShow"
    :membership-level="user.membershipLevel"
    :is-expired="user.isExpired"
  />
</template>

<script>
import Appeal from '../components/Appeal.vue';
import userMixin from '../../store/user/mixin';

export default {
  name: 'AppealContainer',

  components: { Appeal },

  mixins: [userMixin],

  computed: {
    shouldShow() {
      const { isRecurringDonor, isSingleDonor } = this.user;

      return isRecurringDonor || isSingleDonor;
    },
  },
};
</script>
