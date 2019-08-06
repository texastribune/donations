<template>
  <edit-form
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
import EditForm from '../components/EditForm.vue';

export default {
  name: 'EditContactInfoFormContainer',

  components: { EditForm },

  mixins: [userMixin, tokenUserMixin, contextMixin],

  computed: {
    initialFields() {
      const { first_name, last_name, postal_code, identities } = this.user;
      const { email } = this.tokenUser;
      const { tribune_offers_consent } = getTokenIdentity(identities, email);

      return {
        firstName: {
          name: 'firstName',
          label: 'First name',
          value: first_name,
          rules: { required: true },
          isVisible: true,
        },
        lastName: {
          name: 'lastName',
          label: 'Last name',
          value: last_name,
          rules: { required: true },
          isVisible: true,
        },
        zip: {
          name: 'zip',
          label: 'ZIP code',
          value: postal_code,
          rules: { required: true, numeric: true },
          isVisible: true,
        },
        email: {
          name: 'email',
          label: 'Email',
          value: email,
          rules: { required: true, email: true },
          isVisible: true,
        },
        confirmedEmail: {
          name: 'confirmedEmail',
          label: 'Type your email again to confirm the change',
          value: '',
          rules: null,
          isVisible: false,
        },
        marketing: {
          name: 'marketing',
          label:
            'Yes, I would like to receive emails with special promotions, product announcements and membership opportunities.',
          value: tribune_offers_consent,
          rules: {},
          isVisible: true,
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
