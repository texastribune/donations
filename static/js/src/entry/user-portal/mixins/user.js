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
    logIn,
    logOut,
    register,
    resetPassword,
    redirectAfterLogIn,
    redirectAfterLogOut,
    setFlag,
    clearFlag,
  },
};
