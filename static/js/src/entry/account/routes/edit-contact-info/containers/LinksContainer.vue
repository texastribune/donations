<template>
  <links
    :is-blast-subscriber="isBlastSubscriber"
    :is-single-donor="isSingleDonor"
    :is-recurring-donor="isRecurringDonor"
    :is-circle-donor="isCircleDonor"
    :is-staff="isStaff"
    :pw-reset-success="pwResetSuccess"
    :pw-reset-failure="pwResetFailure"
    @resetPassword="resetPassword"
  />
</template>

<script>
/* eslint-disable camelcase */

import Links from '../components/Links.vue';
import userMixin from '../../../store/user/mixin';
import tokenUserMixin from '../../../store/token-user/mixin';
import { resetPassword } from '../../../utils/auth-actions';

export default {
  name: 'EditContactInfoLinksContainer',

  components: { Links },

  mixins: [userMixin, tokenUserMixin],

  data() {
    return {
      pwResetSuccess: false,
      pwResetFailure: false,
    };
  },

  computed: {
    isStaff() {
      return this.tokenUser['https://texastribune.org/is_staff'];
    },

    isBlastSubscriber() {
      return this.user.is_blast_subscriber;
    },

    isSingleDonor() {
      return this.user.is_single_donor;
    },

    isRecurringDonor() {
      return this.user.is_recurring_donor;
    },

    isCircleDonor() {
      return this.user.is_circle_donor;
    },
  },

  methods: {
    resetPassword() {
      const { email } = this.tokenUser;

      resetPassword(email, err => {
        if (err) {
          this.pwResetFailure = true;
        } else {
          this.pwResetSuccess = true;
        }
      });
    },
  },
};
</script>
