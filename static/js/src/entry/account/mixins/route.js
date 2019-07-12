/* eslint-disable camelcase */

import { logIn, logOut } from '../utils/auth-actions';
import tokenUserMixin from './token-user';
import { TITLE_SUFFIX } from '../constants';
import { InvalidRouteError, UnverifiedError } from '../errors';

export default {
  mixins: [tokenUserMixin],

  props: {
    parentRouteIsFetching: {
      type: Boolean,
      required: true,
    },
  },

  data() {
    return {
      routeIsFetching: true,
      shouldLogPV: true,
    };
  },

  async created() {
    const { isProtected, isExact, title } = this.route;
    const {
      accessToken,
      tokenUserError,
      isVerified,
      parentRouteIsFetching,
    } = this;

    // sometimes title will be null in cases
    // where it can't be set until a data fetch happens
    if (isExact && title) this.setTitle();

    if (tokenUserError && isProtected) {
      // Auth0 error encountered during checkSession call
      throw tokenUserError;
    } else if (!accessToken && isProtected) {
      // login-required route; user not logged in
      logIn();
    } else if (!isVerified && isProtected) {
      // login-required route; user has not verified email
      throw new UnverifiedError();
    } else if (!parentRouteIsFetching) {
      // top level route; do data fetch immediately
      // because there's no parent fetch to wait on
      await this.doRouteFetch(this.$route);
    }
  },

  methods: {
    setTitle() {
      const { title } = this.route;
      document.title = `${title} ${TITLE_SUFFIX}`;
    },

    logPageView() {
      window.dataLayer.push({
        event: 'userPortalPageview',
        pagePath: window.location.pathname,
        pageTitle: document.title,
      });
    },

    setRouteIsFetching(routeIsFetching) {
      this.routeIsFetching = routeIsFetching;
    },

    async doRouteFetch(toRoute, next) {
      const { isExact } = this.route;
      const { shouldLogPV } = this;

      try {
        if (next) {
          // if an active route's params have changed
          await this.refetchData(toRoute);
        } else {
          await this.fetchData(toRoute);
        }

        if (next) next();
        if (isExact && shouldLogPV) this.logPageView();

        // we don't want to log a PV again if this
        // data fetch is repeated (unless route params have changed)
        this.shouldLogPV = false;
        this.routeIsFetching = false;
      } catch (err) {
        if (next) next();

        // you're on a route that you're not supposed to be on
        // like the Blast page if you're not a Blast subscriber
        if (err instanceof InvalidRouteError) {
          this.$router.push({ name: 'home' });
        } else {
          throw err;
        }
      }
    },
  },

  watch: {
    // watch the value of accessToken as we refresh
    // it every 15 minutes
    accessToken(newToken, oldToken) {
      const {
        route: { isProtected },
        tokenUserError,
      } = this;

      if (isProtected && oldToken && !newToken) {
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

    async parentRouteIsFetching(newVal, oldVal) {
      // if a child route has a parent that's doing
      // a data fetch, wait for the parent fetch to complete
      // in case the child's fetch depends on data from it
      if (oldVal && !newVal) {
        await this.doRouteFetch(this.$route);
      }
    },
  },

  async beforeRouteUpdate(to, from, next) {
    // to refetch when route params have changed
    // a refetchData method must be defined
    if (!this.refetchData) {
      next();
    } else {
      this.routeIsFetching = true;
      this.shouldLogPV = true;

      await this.doRouteFetch(to, next);
    }
  },
};
