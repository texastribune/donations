<template>
  <logged-out
    v-if="shouldShow"
    :existing-email="existingEmail"
    :email-to-link="emailToLink"
    @logIn="logIn"
  />
</template>

<script>
import tokenUserMixin from '../../../store/token-user/mixin';
import { logIn } from '../../../utils/auth-actions';
import LoggedOut from '../components/LoggedOut.vue';

export default {
  name: 'ConfirmLinkedIdentityLoggedOutContainer',

  components: { LoggedOut },

  mixins: [tokenUserMixin],

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

  computed: {
    shouldShow() {
      return !this.accessToken;
    },
  },

  methods: {
    logIn() {
      logIn(`/account/confirm-linked-identity?ticket=${this.ticket}`);
    },
  },
};
</script>
