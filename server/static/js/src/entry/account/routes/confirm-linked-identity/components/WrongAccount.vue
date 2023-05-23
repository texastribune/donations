<template>
  <div>
    <h1 class="has-xl-btm-marg">You're logged into the wrong account</h1>
    <p class="has-b-btm-marg">
      To link <strong>{{ emailToLink }}</strong> to the Texas Tribune account
      created with <strong>{{ existingEmail }}</strong
      >, you need to log into Texas Tribune account:
      <strong>{{ existingEmail }}</strong
      >. Right now, you're logged into Texas Tribune account:
      <strong>{{ user.email }}</strong
      >.
    </p>
    <p class="has-b-btm-marg">
      Click <strong>LOG OUT</strong> below. You'll be sent to a page where you
      can log in with <strong>{{ existingEmail }}</strong
      >, then complete the account link.
    </p>
    <p class="has-xl-btm-marg">
      If these email addresses don't belong to you, or you didn't mean to do
      this, click <strong>CANCEL</strong> or simply ignore this.
    </p>
    <div class="c-btn-or-btn">
      <div class="c-btn-or-btn__first">
        <base-button
          :display="{ bg: 'gray-light', color: 'black' }"
          text="Log out"
          @onClick="logOut"
        />
      </div>
      <span class="c-btn-or-btn__word t-align-center l-align-center-self"
        >or</span
      >
      <div class="c-btn-or-btn__last">
        <base-button
          :display="{ bg: 'gray-light', color: 'black' }"
          text="Cancel"
          @onClick="goToHomePage"
        />
      </div>
    </div>
  </div>
</template>

<script>
import userMixin from '../../../store/user/mixin';

import { logOut } from '../../../utils/auth-actions';

export default {
  name: 'ConfirmLinkedIdentityWrongAccount',

  mixins: [userMixin],

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

  methods: {
    logOut() {
      logOut({
        redirectName: 'confirmLinkedIdentity',
        redirectQueryParams: { ticket: this.ticket },
      });
    },

    goToHomePage() {
      window.location.href = 'https://www.texastribune.org/';
    },
  },
};
</script>
