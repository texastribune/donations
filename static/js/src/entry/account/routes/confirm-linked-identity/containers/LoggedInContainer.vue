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
import tokenUserMixin from '../../../store/token-user/mixin';
import userMixin from '../../../store/user/mixin';
import contextMixin from '../../../store/context/mixin';
import { CONTEXT_TYPES, USER_TYPES } from '../../../store/types';
import LoggedIn from '../components/LoggedIn.vue';

export default {
  name: 'ConfirmLinkedIdentityLoggedInContainer',

  components: { LoggedIn },

  mixins: [tokenUserMixin, userMixin, contextMixin],

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
      return this.tokenUser.isReady;
    },
  },

  methods: {
    goHome() {
      this.$router.push({ name: 'home' });
    },

    async confirm() {
      this[CONTEXT_TYPES.setIsFetching](true);

      await this[USER_TYPES.confirmLinkedIdentity](this.ticket);

      this[CONTEXT_TYPES.setIsFetching](false);

      this.goHome();
    },
  },
};
</script>
