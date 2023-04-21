<template>
  <div>
    <h1 class="has-xl-btm-marg">To verify, please log in</h1>
    <p class="has-b-btm-marg">
      To link <strong>{{ emailToLink }}</strong> to the Texas Tribune account
      created with <strong>{{ existingEmail }}</strong
      >, please log into your account.
    </p>
    <p class="has-xl-btm-marg">
      If these email addresses don't belong to you, or you didn't mean to do
      this, click <strong>CANCEL</strong> or simply ignore this.
    </p>
    <div class="c-btn-or-btn">
      <div class="c-btn-or-btn__first">
        <base-button
          :display="{ bg: 'gray-light', color: 'black' }"
          text="Log in"
          @onClick="logIn"
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
import { logIn } from '../../../utils/auth-actions';

export default {
  name: 'ConfirmLinkedIdentityLoggedOut',

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
    logIn() {
      window.dataLayer.push({
        event: this.ga.customEventName,
        gaCategory: this.ga.userPortal.category,
        gaAction: this.ga.userPortal.actions['login-linked-email'],
        gaLabel: this.ga.userPortal.labels['login-linked-identity'],
      });

      logIn({
        redirectName: 'confirmLinkedIdentity',
        redirectQueryParams: { ticket: this.ticket },
      });
    },

    goToHomePage() {
      window.dataLayer.push({
        event: this.ga.customEventName,
        gaCategory: this.ga.userPortal.category,
        gaAction: this.ga.userPortal.actions['cancel-linked-email'],
        gaLabel: this.ga.userPortal.labels['login-linked-identity'],
      });

      window.location.href = 'https://www.texastribune.org/';
    },
  },
};
</script>
