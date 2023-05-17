import tokenUserMixin from '../store/token-user/mixin';

import { logOut } from '../utils/auth-actions';

import { REDIRECTS_META } from '../constants';

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

  methods: {
    redirectFromQueryParams() {
      const { redirectName, redirectQueryParams } = this.$route.query;
      const redirectMeta = REDIRECTS_META[redirectName];

      if (redirectMeta) {
        const { external, url, routeName } = redirectMeta;

        setTimeout(() => {
          if (external) {
            window.location.href = url;
          } else {
            this.$router.push({
              name: routeName,
              query: redirectQueryParams
                ? JSON.parse(decodeURIComponent(redirectQueryParams))
                : {},
            });
          }
        }, 1800);
      }
    },
  },
};
