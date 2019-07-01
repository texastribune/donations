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
      let name;
      let nameHeading;
      let finalEmail;
      let username;

      const { isViewingAs } = this;
      const { email: tokenEmail } = this.tokenUser;
      const { identities, postal_code, first_name, last_name } = this.user;
      const [goodIdentity] = identities.filter(
        ({ email: apiEmail }) => apiEmail === tokenEmail
      );

      try {
        ({ email: finalEmail, username } = goodIdentity);
      } catch (err) {
        // if we're using "view as" feature, it's expected that
        // the ID-token email won't match up with the API email
        if (isViewingAs) {
          finalEmail = identities[0].email;
          // eslint-disable-next-line prefer-destructuring
          username = identities[0].username;
        } else {
          throw err;
        }
      }

      if (first_name && last_name) {
        nameHeading = 'Name';
        // eslint-disable-next-line camelcase
        name = `${first_name} ${last_name}`;
      } else {
        nameHeading = 'Username';
        name = username;
      }

      const contactInfo = [
        { id: 0, heading: nameHeading, text: name },
        { id: 1, heading: 'Email', text: finalEmail },
      ];

      if (postal_code) {
        contactInfo.push({ id: 2, heading: 'ZIP code', text: postal_code });
      }

      return contactInfo;
    },
  },
};
</script>
