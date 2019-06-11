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
      // eslint-disable-next-line camelcase
      const { given_name, family_name, email, nickname } = this.tokenUser;
      // eslint-disable-next-line camelcase
      const { postal_code } = this.user;

      // eslint-disable-next-line camelcase
      if (given_name && family_name) {
        nameHeading = 'Name';
        // eslint-disable-next-line camelcase
        name = `${given_name} ${family_name}`;
      } else {
        nameHeading = 'Username';
        name = nickname;
      }

      const contactInfo = [
        { id: 0, heading: nameHeading, text: name },
        { id: 1, heading: 'Email', text: email },
      ];

      // eslint-disable-next-line camelcase
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
