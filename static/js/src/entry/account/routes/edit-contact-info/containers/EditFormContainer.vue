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
import { AxiosResponseError } from '../../../errors';
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
        firstName: first_name || '',
        lastName: last_name || '',
        email,
        confirmedEmail: '',
        zip: postal_code || '',
        marketing: tribune_offers_consent,
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
      const newEmail = identityPayload.email;

      if (Object.keys(userPayload).length > 0) {
        dispatches.push(this.updateUser(userPayload));
      }

      if (Object.keys(identityPayload).length > 0) {
        dispatches.push(this.updateIdentity(identityPayload));
      }

      if (dispatches.length) {
        await this.updateContactInfo(dispatches, newEmail);
        this.logToGtm(fields);
      }
    },

    async updateContactInfo(dispatches, newEmail) {
      let badEmailUpdate = false;

      this.setAppIsFetching(true);

      try {
        await Promise.all(dispatches);
      } catch (err) {
        if (
          err instanceof AxiosResponseError &&
          err.status === 400 &&
          err.data.detail === "can't change email"
        ) {
          badEmailUpdate = true;
        } else {
          throw err;
        }
      }

      if (newEmail && !badEmailUpdate) {
        logOut(`/account/changed-email?email=${encodeURIComponent(newEmail)}`);
      } else if (newEmail && badEmailUpdate) {
        this.badEmail = newEmail;
      } else if (!newEmail) {
        this.showSuccess = true;
      }

      await this.getUser();

      this.setAppIsFetching(false);
    },

    logToGtm(fields) {
      const allEvents = [];
      const baseEvent = {
        event: this.ga.customEventName,
        gaCategory: this.ga.userPortal.category,
        gaLabel: this.ga.userPortal.labels['edit-contact-info'],
      };

      if (fields.email.changed) {
        allEvents.push({
          ...baseEvent,
          gaAction: this.ga.userPortal.actions['edit-email'],
        });
      }
      if (fields.firstName.changed || fields.lastName.changed) {
        allEvents.push({
          ...baseEvent,
          gaAction: this.ga.userPortal.actions['edit-name'],
        });
      }
      if (fields.zip.changed) {
        allEvents.push({
          ...baseEvent,
          gaAction: this.ga.userPortal.actions['edit-zip'],
        });
      }

      if (fields.marketing.changed && fields.marketing.value) {
        allEvents.push({
          ...baseEvent,
          gaAction: this.ga.userPortal.actions['marketing-opt-in'],
        });
      }
      if (fields.marketing.changed && !fields.marketing.value) {
        allEvents.push({
          ...baseEvent,
          gaAction: this.ga.userPortal.actions['marketing-opt-out'],
        });
      }

      allEvents.forEach(event => {
        window.dataLayer.push(event);
      });
    },
  },
};
</script>
