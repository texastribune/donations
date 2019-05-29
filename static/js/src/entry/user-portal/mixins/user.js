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
      const { idToken, accessToken, details } = this.$store.state.user;

      return {
        idToken,
        accessToken,
        details,
        logIn,
        logOut,
        register,
        resetPassword,
        redirectAfterLogIn,
        redirectAfterLogOut,
        setFlag,
        clearFlag,
      };
    },
  },
};
