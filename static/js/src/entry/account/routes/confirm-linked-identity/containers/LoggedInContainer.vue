<template>
  <logged-in
    v-if="shouldShow"
    :existing-email="existingEmail"
    :email-to-link="emailToLink"
    @goHome="goHome"
    @confirm="confirm"
  />
</template>

<script>
/* eslint-disable camelcase */

import jwt from 'jsonwebtoken';

import tokenUserMixin from '../../../store/token-user/mixin';
import userMixin from '../../../store/user/mixin';
import contextMixin from '../../../store/context/mixin';
import LoggedIn from '../components/LoggedIn.vue';

export default {
  name: 'ConfirmLinkedIdentityLoggedInContainer',

  components: { LoggedIn },

  mixins: [tokenUserMixin, userMixin, contextMixin],

  props: {
    ticket: {
      type: String,
      required: true,
    },
  },

  computed: {
    shouldShow() {
      return !!this.accessToken;
    },

    existingEmail() {
      const { existing_email } = jwt.decode(this.ticket);
      return existing_email;
    },

    emailToLink() {
      const { email_to_link } = jwt.decode(this.ticket);
      return email_to_link;
    },
  },

  methods: {
    async confirm() {
      this.setAppIsFetching(true);

      await this.confirmLinkedIdentity(this.ticket);

      this.setAppIsFetching(false);
      this.goHome();
    },

    goHome() {
      this.$emit('goHome');
    },
  },
};
</script>
