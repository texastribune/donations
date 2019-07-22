<template>
  <contact-info-form
    :initial-values="initialValues"
    @updateContactInfo="updateContactInfo"
  />
</template>

<script>
/* eslint-disable camelcase */

import userMixin from '../../../store/user/mixin';
import tokenUserMixin from '../../../store/token-user/mixin';
import contextMixin from '../../../store/context/mixin';
import getTokenIdentity from '../../../utils/get-token-identity';
import { setChangedEmailFlag } from '../../../utils/change-email';
import { logOut } from '../../../utils/auth-actions';
import ContactInfoForm from '../components/ContactInfoForm.vue';

export default {
  name: 'AccountFormContainer',

  components: { ContactInfoForm },

  mixins: [userMixin, tokenUserMixin, contextMixin],

  computed: {
    initialValues() {
      const { first_name, last_name, postal_code, identities } = this.user;
      const { email: tokenEmail } = this.tokenUser;
      const { tribune_offers_consent } = getTokenIdentity(
        identities,
        tokenEmail
      );

      return {
        firstName: first_name,
        lastName: last_name,
        zip: postal_code,
        email: tokenEmail,
        marketing: tribune_offers_consent,
      };
    },
  },

  methods: {
    async updateContactInfo({ userPayload, identityPayload }) {
      this.setAppIsFetching(true);

      await Promise.all([
        this.updateUser(userPayload),
        this.updateIdentity(identityPayload),
      ]);

      const { email } = identityPayload;

      if (email) {
        setChangedEmailFlag(email);
        logOut();
      } else {
        await this.getUser();
      }

      this.setAppIsFetching(false);
    },
  },
};
</script>
