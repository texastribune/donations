<template>
  <edit-contact-info-form
    :initial-fields="initialFields"
    @onSubmit="onSubmit"
    @onFormHasChangedToggle="setShowModal"
  />
</template>

<script>
/* eslint-disable camelcase */

import userMixin from '../../../store/user/mixin';
import tokenUserMixin from '../../../store/token-user/mixin';
import contextMixin from '../../../store/context/mixin';
import getTokenIdentity from '../../../utils/get-token-identity';
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
        firstName: {
          value: first_name,
          isVisible: true,
          shouldValidate: true,
        },
        lastName: {
          value: last_name,
          isVisible: true,
          shouldValidate: true,
        },
        zip: {
          value: postal_code,
          isVisible: true,
          shouldValidate: true,
        },
        email: {
          value: tokenEmail,
          isVisible: true,
          shouldValidate: true,
        },
        confirmedEmail: {
          value: '',
          isVisible: false,
          shouldValidate: true,
        },
        marketing: {
          value: tribune_offers_consent,
          isVisible: true,
          shouldValidate: false,
        },
      };
    },
  },

  methods: {
    setShowModal(formHasChanged) {
      this.$emit('setShowModal', formHasChanged);
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

      if (fields.email.changed) {
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
        logOut(`/account/changed-email?email=${email}`);
      } else {
        await this.getUser();
      }

      this.setAppIsFetching(false);
    },
  },
};
</script>
