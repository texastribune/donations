<template>
  <loader v-if="isFetching" />

  <div v-else>
    <h1 class="has-xl-btm-marg">Are you sure?</h1>
    <p class="has-b-btm-marg">
      You're about to link <strong>{{ emailToLink }}</strong> to Texas Tribune
      account: <strong>{{ existingEmail }}</strong
      >. Click below to confirm this update to your account.
    </p>
    <p class="has-xl-btm-marg">
      If these email addresses don't belong to you, or you didn't mean to do
      this, click <strong>CANCEL</strong> or simply ignore this.
    </p>
    <div class="c-btn-or-btn">
      <div class="c-btn-or-btn__first">
        <base-button
          :display="{ bg: 'gray-light', color: 'black' }"
          text="Confirm email link"
          @onClick="confirm"
        />
      </div>
      <span class="c-btn-or-btn__word t-align-center l-align-center-self"
        >or</span
      >
      <div class="c-btn-or-btn__last">
        <base-button
          :display="{ bg: 'gray-light', color: 'black' }"
          text="Cancel"
          @onClick="cancel"
        />
      </div>
    </div>
  </div>
</template>

<script>
import userMixin from '../../../store/user/mixin';
import contextMixin from '../../../store/context/mixin';

import Loader from './Loader.vue';

import { CONTEXT_TYPES, USER_TYPES } from '../../../store/types';

export default {
  name: 'ConfirmLinkedIdentityReady',

  components: { Loader },

  mixins: [userMixin, contextMixin],

  props: {
    existingEmail: {
      type: String,
      required: true,
    },

    emailToLink: {
      type: String,
      required: true,
    },

    ticket: {
      type: String,
      required: true,
    },
  },

  data() {
    return { isFetching: true };
  },

  async mounted() {
    await this[USER_TYPES.getUser]();
    this.isFetching = false;
  },

  methods: {
    async confirm() {
      window.dataLayer.push({
        event: this.ga.customEventName,
        gaCategory: this.ga.userPortal.category,
        gaAction: this.ga.userPortal.actions['confirm-linked-email'],
        gaLabel: this.ga.userPortal.labels['confirm-linked-identity'],
      });

      this[CONTEXT_TYPES.setIsFetching](true);
      await this[USER_TYPES.confirmLinkedIdentity](this.ticket);
      this[CONTEXT_TYPES.setIsFetching](false);

      this.$router.push({ name: 'accountOverview' });
    },

    cancel() {
      window.dataLayer.push({
        event: this.ga.customEventName,
        gaCategory: this.ga.userPortal.category,
        gaAction: this.ga.userPortal.actions['cancel-linked-email'],
        gaLabel: this.ga.userPortal.labels['confirm-linked-identity'],
      });

      this.$router.push({ name: 'accountOverview' });
    },
  },
};
</script>
