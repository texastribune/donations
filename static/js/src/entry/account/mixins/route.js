/* eslint-disable camelcase */

import { logOut } from '../utils/auth-actions';
import tokenUserMixin from '../store/token-user/mixin';
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
    return { routeIsFetching: true };
  },

  async created() {
    if (!this.parentRouteIsFetching) {
      console.log('created', this.$route);
      // top level route; do data fetch immediately
      // because there's no parent fetch to wait on
      await this.doRouteFetch();
    }
  },

  methods: {
    logPageView() {
      window.dataLayer.push({
        event: 'userPortalPageview',
        pagePath: window.location.pathname,
        pageTitle: document.title,
      });
    },

    async doRouteFetch() {
      console.log('hi');
      try {
        this.routeIsFetching = true;

        await this.fetchData(this.$route);

        if (this.$route.meta.isExact) this.logPageView();

        this.routeIsFetching = false;
      } catch (err) {
        // you're on a route that you're not supposed to be on
        // like the Blast page if you're not a Blast subscriber
        if (err instanceof InvalidRouteError) {
          this.$router.push({ name: 'home' });
        } else {
          throw err;
        }
      }
    },

    // eslint-disable-next-line no-empty-function
    async fetchData() {},
  },

  watch: {
    // watch the value of accessToken as we refresh
    // it every 15 minutes
    accessToken(newToken, oldToken) {
      const { tokenUserError } = this;
      const { isProtected } = this.$route.meta;

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

    async parentRouteIsFetching(newParentIsFetching, oldParentIsFetching) {
      // if a child route has a parent that's doing
      // a data fetch, wait for the parent fetch to complete
      // in case the child's fetch depends on data from it
      if (oldParentIsFetching && !newParentIsFetching) {
        console.log('parent', this.$route);
        await this.doRouteFetch();
      }
    },
  },

  metaInfo() {
    return {
      title: this.$route.meta.title,
    };
  },
};
