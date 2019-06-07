<template>
  <contact-info
    :pw-reset-success="pwResetSuccess"
    :pw-reset-failure="pwResetFailure"
    :contact-info="contactInfo"
    @resetPassword="resetPassword"
  />
</template>

<script>
import ContactInfo from '../components/ContactInfo.vue';
import userMixin from '../../home/mixins/user';
import { resetPassword } from '../../../utils/auth-actions';

export default {
  name: 'ContactInfoContainer',

  components: { ContactInfo },

  mixins: [userMixin],

  data() {
    return { pwResetSuccess: false, pwResetFailure: false };
  },

  computed: {
    contactInfo() {
      let name;
      let nameHeading;
      // eslint-disable-next-line camelcase
      const { first_name, last_name, identities, postal_code } = this.user;
      const allEmails = identities.map(({ email }) => email);
      const formattedEmails = allEmails.join(', ');

      // eslint-disable-next-line camelcase
      if (first_name && last_name) {
        nameHeading = 'Name';
        // eslint-disable-next-line camelcase
        name = `${first_name} ${last_name}`;
      } else {
        nameHeading = 'Username';
        name = identities[0].username;
      }

      const contactInfo = [
        { id: 0, heading: nameHeading, text: name },
        { id: 1, heading: 'Email', text: formattedEmails },
      ];

      // eslint-disable-next-line camelcase
      if (postal_code) {
        contactInfo.push({ id: 2, heading: 'ZIP code', text: postal_code });
      }

      return contactInfo;
    },
  },

  methods: {
    resetPassword() {
      const { identities } = this.user;

      resetPassword(identities[0].email, err => {
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
