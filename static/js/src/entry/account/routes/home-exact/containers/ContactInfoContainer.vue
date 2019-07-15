<template>
  <contact-info
    :pw-reset-success="pwResetSuccess"
    :pw-reset-failure="pwResetFailure"
    :contact-info="contactInfo"
    :is-staff="isStaff"
    @resetPassword="resetPassword"
  />
</template>

<script>
/* eslint-disable camelcase */

import { mapState } from 'vuex';

import ContactInfo from '../components/ContactInfo.vue';
import tokenUserMixin from '../../../mixins/token-user';
import userMixin from '../../home/mixins/user';
import { resetPassword } from '../../../utils/auth-actions';

export default {
  name: 'ContactInfoContainer',

  components: { ContactInfo },

  mixins: [tokenUserMixin, userMixin],

  data() {
    return {
      pwResetSuccess: false,
      pwResetFailure: false,
      contactInfo: [],
    };
  },

  computed: {
    ...mapState('context', ['isViewingAs']),

    isStaff() {
      return this.tokenUser['https://texastribune.org/is_staff'];
    },
  },

  watch: {
    isViewingAs() {
      this.contactInfo = this.getContactInfo();
    },
  },

  created() {
    this.contactInfo = this.getContactInfo();
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

      window.dataLayer.push({
        event: this.ga.customEventName,
        gaCategory: this.ga.userPortal.category,
        gaAction: this.ga.userPortal.actions['reset-password'],
        gaLabel: this.ga.userPortal.labels.home,
      });
    },

    getContactInfo() {
      let email;
      let username;

      const contactInfo = [];
      const { isViewingAs } = this;
      const { email: tokenEmail } = this.tokenUser;
      const { identities, postal_code, first_name, last_name } = this.user;
      const [goodIdentity] = identities.filter(
        ({ email: apiEmail }) => apiEmail === tokenEmail
      );

      try {
        ({ email, username } = goodIdentity);
      } catch (err) {
        // if we're using "view as" feature, it's expected that
        // the ID-token email won't match up with the API email
        if (isViewingAs) {
          ({ email, username } = identities[0]);
        } else {
          throw err;
        }
      }

      if (first_name && last_name) {
        contactInfo.push({
          id: 0,
          heading: 'Name',
          text: `${first_name} ${last_name}`,
        });
      } else {
        contactInfo.push({
          id: 0,
          heading: 'Username',
          text: username,
        });
      }

      contactInfo.push({ id: 1, heading: 'Email', text: email });

      if (postal_code) {
        contactInfo.push({ id: 2, heading: 'ZIP code', text: postal_code });
      }

      return contactInfo;
    },
  },
};
</script>
