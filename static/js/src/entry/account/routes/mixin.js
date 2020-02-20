import { logOut } from '../utils/auth-actions';
import tokenUserMixin from '../store/token-user/mixin';

export default {
  mixins: [tokenUserMixin],

  data() {
    return { routeIsFetching: true };
  },

  computed: {
    isLoggedIn() {
      return this.tokenUser.isLoggedIn;
    },

    tokenUserError() {
      return this.tokenUser.error;
    },
  },

  async mounted() {
    if (this.hasRouteFetch) {
      await this.fetchData();
    }

    this.routeIsFetching = false;
  },

  watch: {
    isLoggedIn(newIsLoggedIn, oldIsLoggedIn) {
      const { isProtected } = this.$route.meta;

      if (isProtected && oldIsLoggedIn && !newIsLoggedIn) {
        logOut();
      }
    },

    tokenUserError(newTokenUserError, oldTokenUserError) {
      const { isProtected } = this.$route.meta;

      if (isProtected && newTokenUserError && !oldTokenUserError) {
        throw this.tokenUserError;
      }
    },
  },
};
