<template>
  <profile-settings :contact-info="contactInfo" />
</template>

<script>
/* eslint-disable camelcase */

import { mapState } from 'vuex';

import ProfileSettings from '../components/ProfileSettings.vue';
import tokenUserMixin from '../../../store/token-user/mixin';
import userMixin from '../../../store/user/mixin';

export default {
  name: 'SummmaryProfileSettingsContainer',

  components: { ProfileSettings },

  mixins: [tokenUserMixin, userMixin],

  computed: {
    ...mapState('context', ['isViewingAs']),

    contactInfo() {
      let email;

      const contactInfo = [];
      const { isViewingAs } = this;
      const { identities, postal_code, first_name, last_name } = this.user;

      if (isViewingAs) {
        email = identities[0].email;
      } else {
        email = this.tokenUser.email;
      }

      if (first_name && last_name) {
        contactInfo.push({
          id: 0,
          heading: 'Name',
          text: `${first_name} ${last_name}`,
        });
      }

      contactInfo.push({ id: 1, heading: 'Login email', text: email });

      if (postal_code) {
        contactInfo.push({ id: 2, heading: 'ZIP code', text: postal_code });
      }

      return contactInfo;
    },
  },
};
</script>
