import {
  logIn,
  logOut,
  register,
  setFlag,
  clearFlag,
  resetPassword,
  redirectAfterLogIn,
  redirectAfterLogOut,
} from '../utils/auth-actions';

export default {
  computed: {
    user() {
      const { token, details } = this.$store.state.user;
      return { token, details };
    },
  },

  methods: {
    logIn() {
      logIn();
    },

    logOut() {
      logOut();
    },

    register() {
      register();
    },

    resetPassword(opts, cb) {
      resetPassword(opts, cb);
    },

    redirectAfterLogIn() {
      redirectAfterLogIn();
    },

    redirectAfterLogOut() {
      redirectAfterLogOut();
    },

    setFlag() {
      setFlag();
    },

    clearFlag() {
      clearFlag();
    },
  },
};
