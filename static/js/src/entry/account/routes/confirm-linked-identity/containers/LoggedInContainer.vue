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
      return !!this.accessToken;
    },
  },

  methods: {
    goHome() {
      this.$emit('goHome');
    },

    async confirm() {
      this.setAppIsFetching(true);

      await this.confirmLinkedIdentity(this.ticket);

      this.setAppIsFetching(false);
      this.goHome();
    },
  },
};
</script>
