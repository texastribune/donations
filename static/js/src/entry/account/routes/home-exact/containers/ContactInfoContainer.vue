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

import ContactInfo from '../components/ContactInfo.vue';
import tokenUserMixin from '../../../mixins/token-user';
import userMixin from '../../home/mixins/user';
import { resetPassword } from '../../../utils/auth-actions';

export default {
  name: 'ContactInfoContainer',

  components: { ContactInfo },

  mixins: [tokenUserMixin, userMixin],

  data() {
    return { pwResetSuccess: false, pwResetFailure: false };
  },

  computed: {
    contactInfo() {
      let name;
      let nameHeading;
      let finalEmail;
      let username;

      const { email: tokenEmail } = this.tokenUser;
      const { identities, postal_code, first_name, last_name } = this.user;
      const [goodIdentity] = identities.filter(
        ({ email: apiEmail }) => apiEmail === tokenEmail
      );

      try {
        ({ email: finalEmail, username } = goodIdentity);
      } catch (err) {
        // we're viewing as someone else
        finalEmail = identities[0].email;
        // eslint-disable-next-line prefer-destructuring
        username = identities[0].username;
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

    isStaff() {
      return this.tokenUser['https://texastribune.org/is_staff'];
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
