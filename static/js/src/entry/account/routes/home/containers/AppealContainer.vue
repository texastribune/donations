<template>
  <appeal v-if="shouldShow" :level="level" :is-expired="isExpired" />
</template>

<script>
/* eslint-disable camelcase */

import Appeal from '../components/Appeal.vue';
import userMixin from '../mixins/user';

export default {
  name: 'AppealContainer',

  components: { Appeal },

  mixins: [userMixin],

  computed: {
    level() {
      return this.user.membership_level;
    },

    isExpired() {
      return this.user.is_expired;
    },

    shouldShow() {
      const { is_recurring_donor, is_single_donor } = this.user;

      return is_recurring_donor || is_single_donor;
    },
  },
};
</script>
