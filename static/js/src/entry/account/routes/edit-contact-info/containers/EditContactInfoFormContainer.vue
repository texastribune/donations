<template>
  <edit-contact-info-form
    :initial-fields="initialFields"
    @onSubmit="onSubmit"
    @onHasChangedToggle="setShowModal"
  />
</template>

<script>
/* eslint-disable camelcase */

import userMixin from '../../../store/user/mixin';
import tokenUserMixin from '../../../store/token-user/mixin';
import contextMixin from '../../../store/context/mixin';
import getTokenIdentity from '../../../utils/get-token-identity';
import { setChangedEmail } from '../../../utils/storage';
import { logOut } from '../../../utils/auth-actions';
import EditContactInfoForm from '../components/EditContactInfoForm.vue';

export default {
  name: 'EditContactInfoFormContainer',

  components: { EditContactInfoForm },

  mixins: [userMixin, tokenUserMixin, contextMixin],

  computed: {
    initialFields() {
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
        confirmedEmail: '',
        marketing: tribune_offers_consent,
      };
    },
  },

  methods: {
    setShowModal(shouldShow) {
      this.$emit('setShowModal', shouldShow);
    },

    async onSubmit(fields) {
      const userPayload = {
        first_name: fields.firstName.value,
        last_name: fields.lastName.value,
        postal_code: fields.zip.value,
      };
      const identityPayload = {
        tribune_offers_consent: fields.marketing.value,
      };

      if (fields.email.flags.changed) {
        identityPayload.email = fields.email.value;
      }

      await this.updateContactInfo({ userPayload, identityPayload });
    },

    async updateContactInfo({ userPayload, identityPayload }) {
      this.setAppIsFetching(true);

      await Promise.all([
        this.updateUser(userPayload),
        this.updateIdentity(identityPayload),
      ]);

      const { email } = identityPayload;

      if (email) {
        setChangedEmail(email);
        logOut();
      } else {
        await this.getUser();
      }

      this.setAppIsFetching(false);
    },
  },
};
</script>
