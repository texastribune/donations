<template>
  <edit-form
    :initial-fields="initialFields"
    :bad-email="badEmail"
    :show-success="showSuccess"
    @onSubmit="onSubmit"
    @onFormHasChangedToggle="setShowModal"
    @onFormIsPristineToggle="resetBadEmailAndSuccess"
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

  data() {
    return { badEmail: '', showSuccess: false };
  },

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
          label: 'Login email',
          value: email,
          rules: { required: true, email: true },
          isVisible: true,
        },
        confirmedEmail: {
          name: 'confirmedEmail',
          label: 'Type your email again to confirm this change',
          value: '',
          isVisible: false,
        },
        marketing: {
          name: 'marketing',
          label:
            "Yes, I'd like to be among the first to know about special announcements, events and membership news from the Tribune. (Important: We will never share your contact info.)",
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

    resetBadEmailAndSuccess(formIsPristine) {
      if (!formIsPristine) {
        this.badEmail = '';
        this.showSuccess = false;
      }
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
      let badEmailUpdate = false;

      this.setAppIsFetching(true);
      this.resetBadEmailAndSuccess();

      try {
        await Promise.all([
          this.updateUser(userPayload),
          this.updateIdentity(identityPayload),
        ]);
      } catch (err) {
        // TODO: Confirm error response
        if (err.response && err.response.status === 400) {
          badEmailUpdate = true;
        } else {
          throw err;
        }
      }

      await this.getUser();

      const { email } = identityPayload;

      if (badEmailUpdate) {
        this.badEmail = email;
      } else if (email) {
        logOut(`/account/changed-email?email=${email}`);
      } else {
        this.showSuccess = true;
      }

      this.setAppIsFetching(false);
    },
  },
};
</script>
