import { logOut } from '../utils/auth-actions';
import logError from '../utils/log-error';
import tokenUserMixin from '../store/token-user/mixin';
import contextMixin from '../store/context/mixin';
import { InvalidRouteError } from '../errors';
import { TITLE_SUFFIX } from '../constants';

export default {
  mixins: [tokenUserMixin, contextMixin],

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
      // top level route; do data fetch immediately
      // because there's no parent fetch to wait on
      await this.doRouteFetch();
    }
  },

  methods: {
    setTitle() {
      document.title = `${this.title} ${TITLE_SUFFIX}`;
    },

    logPageView() {
      window.dataLayer.push({
        event: 'userPortalPageview',
        pagePath: window.location.pathname,
        pageTitle: document.title,
      });
    },

    async doRouteFetch() {
      this.routeIsFetching = true;

      try {
        await this.fetchData();

        if (this.title) {
          this.setTitle();
          this.logPageView();
        }

        this.routeIsFetching = false;
      } catch (err) {
        if (err instanceof InvalidRouteError) {
          this.$router.push({ name: 'home' });
        } else {
          // TODO: throw to errorCaptured in <App />
          this.setAppError(err);
          logError(err);
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
        await this.doRouteFetch();
      }
    },
  },
};
