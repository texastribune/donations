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
          value: first_name || '',
          rules: { required: true },
          isVisible: true,
        },
        lastName: {
          name: 'lastName',
          label: 'Last name',
          value: last_name || '',
          rules: { required: true },
          isVisible: true,
        },
        zip: {
          name: 'zip',
          label: 'ZIP code',
          value: postal_code || '',
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
            "Yes, I'd like to be among the first to know about special announcements, events and membership news from the Tribune. (Remember: Per our privacy policy, we won't share your data without permission.)",
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

    getUserPayload(fields) {
      const userPayload = {};

      if (fields.firstName.changed) {
        userPayload.first_name = fields.firstName.value;
      }

      if (fields.lastName.changed) {
        userPayload.last_name = fields.lastName.value;
      }

      if (fields.zip.changed) {
        userPayload.postal_code = fields.zip.value;
      }

      return userPayload;
    },

    getIdentityPayload(fields) {
      const identityPayload = {};

      if (fields.email.changed) {
        identityPayload.email = fields.email.value;
      }

      if (fields.marketing.changed) {
        identityPayload.tribune_offers_consent = fields.marketing.value;
      }

      return identityPayload;
    },

    async onSubmit(fields) {
      const dispatches = [];
      const userPayload = this.getUserPayload(fields);
      const identityPayload = this.getIdentityPayload(fields);
      const newEmail = identityPayload.email || null;

      if (Object.keys(userPayload).length > 0) {
        dispatches.push(this.updateUser(userPayload));
      }

      if (Object.keys(identityPayload).length > 0) {
        dispatches.push(this.updateIdentity(identityPayload));
      }

      await this.updateContactInfo(dispatches, newEmail);
    },

    async updateContactInfo(dispatches, newEmail) {
      let badEmailUpdate = false;

      this.setAppIsFetching(true);
      this.resetBadEmailAndSuccess();

      try {
        await Promise.all(dispatches);
      } catch (err) {
        if (
          err.response &&
          err.response.status === 400 &&
          err.response.data.detail === "can't change email"
        ) {
          badEmailUpdate = true;
        } else {
          throw err;
        }
      }

      if (newEmail && !badEmailUpdate) {
        logOut(`/account/changed-email?email=${encodeURIComponent(newEmail)}`);
      } else {
        await this.getUser();

        if (badEmailUpdate) {
          this.badEmail = newEmail;
        } else {
          this.showSuccess = true;
        }

        this.setAppIsFetching(false);
      }
    },
  },
};
</script>
