import { logOut } from '../utils/auth-actions';
import tokenUserMixin from '../store/token-user/mixin';

export default {
  mixins: [tokenUserMixin],

  computed: {
    isLoggedIn() {
      return this.tokenUser.isLoggedIn;
    },
  },

  watch: {
    // watch the value of isLoggedIn as we refresh
    // it every 15 minutes
    isLoggedIn(newIsLoggedIn, oldIsLoggedIn) {
      const { error: tokenUserError } = this.tokenUser;
      const { isProtected } = this.$route.meta;

      if (isProtected && oldIsLoggedIn && !newIsLoggedIn) {
        if (tokenUserError) {
          // Auth0 error encountered and user is on a
          // log-in-required route; show error page
          // TODO: show modal
          throw tokenUserError;
        } else {
          // user is on a login-required route and
          // either their session has expired or they
          // have logged out elsewhere; log them out here too
          // TODO: show modal
          logOut();
        }
      }
    },
  },
};
