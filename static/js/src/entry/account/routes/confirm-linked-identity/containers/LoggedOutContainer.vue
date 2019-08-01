<template>
  <logged-out v-if="shouldShow" @logIn="logIn" />
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
