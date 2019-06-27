/* eslint-disable camelcase */

import { mapActions } from 'vuex';

import { logIn, logOut } from '../utils/auth-actions';
import tokenUserMixin from './token-user';
import { TITLE_SUFFIX } from '../constants';
import { InvalidRouteError } from '../errors';

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
    const { email_verified } = this.tokenUser;
    const { accessToken, parentRouteIsFetching } = this;

    // sometimes title will be null in cases
    // where it can't be set until a data fetch happens
    if (isExact && title) this.setTitle();

    if (!accessToken && isProtected) {
      // login-required route; user not logged in
      logIn();
    } else if (!email_verified && isProtected) {
      // login-required route; user has not verified email
      this.setUnverified();
    } else if (!parentRouteIsFetching) {
      // top level route; do data fetch immediately
      // because there's no parent fetch to wait on
      await this.doRouteFetch(this.$route);
    }
  },

  methods: {
    ...mapActions('context', ['setUnverified']),

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
          // if a route's params have changed
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
    accessToken(newToken, oldToken) {
      const {
        route: { isProtected },
      } = this;

      // if users have been logged out somewhere else
      // log them out here too
      if (isProtected && oldToken && !newToken) logOut();
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
