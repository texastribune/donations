<template>
  <links
    :is-single-donor="isSingleDonor"
    :is-recurring-donor="isRecurringDonor"
    :is-circle-donor="isCircleDonor"
    :is-never-given="isNeverGiven"
  />
</template>

<script>
/* eslint-disable camelcase */

import Links from '../components/Links.vue';
import userMixin from '../../../store/user/mixin';

export default {
  name: 'AmbassadorLinksContainer',

  components: { Links },

  mixins: [userMixin],

  computed: {
    isSingleDonor() {
      return this.user.is_single_donor;
    },

    isRecurringDonor() {
      return this.user.is_recurring_donor;
    },

    isCircleDonor() {
      return this.user.is_circle_donor;
    },

    isNeverGiven() {
      return this.user.never_given;
    },
  },
};
</script>
