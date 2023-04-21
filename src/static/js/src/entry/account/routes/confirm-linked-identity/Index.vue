<template>
  <div>
    <basic-nav-bar />

    <main class="l-minimal has-bg-white-off has-xl-padding">
      <div class="l-minimal__content">
        <ready
          v-if="showReady"
          :existing-email="existingEmail"
          :email-to-link="emailToLink"
          :ticket="ticket"
        />
        <logged-out
          v-if="showLoggedOut"
          :existing-email="existingEmail"
          :email-to-link="emailToLink"
          :ticket="ticket"
        />
        <wrong-account
          v-if="showWrongAccount"
          :existing-email="existingEmail"
          :email-to-link="emailToLink"
          :ticket="ticket"
        />
      </div>
    </main>

    <basic-site-footer />
  </div>
</template>

<script>
import jwt from 'jsonwebtoken';

import tokenUserMixin from '../../store/token-user/mixin';
import userMixin from '../../store/user/mixin';
import routeMixin from '../mixin';

import Ready from './components/Ready.vue';
import LoggedOut from './components/LoggedOut.vue';
import WrongAccount from './components/WrongAccount.vue';

export default {
  name: 'ConfirmLinkedIdentityRoute',

  components: { Ready, LoggedOut, WrongAccount },

  mixins: [routeMixin, userMixin, tokenUserMixin],

  computed: {
    ticket() {
      return this.$route.query.ticket;
    },

    existingEmail() {
      const { existing_email: existingEmail } = jwt.decode(this.ticket);
      return existingEmail;
    },

    emailToLink() {
      const { email_to_link: emailToLink } = jwt.decode(this.ticket);
      return emailToLink;
    },

    isRightAccount() {
      return this.existingEmail === this.user.email;
    },

    showReady() {
      return this.tokenUser.isReady && this.isRightAccount;
    },

    showLoggedOut() {
      return !this.tokenUser.isLoggedIn;
    },

    showWrongAccount() {
      return this.tokenUser.isReady && !this.isRightAccount;
    },
  },

  mounted() {
    if (this.tokenUser.error) {
      throw this.tokenUser.error;
    }
  },
};
</script>
