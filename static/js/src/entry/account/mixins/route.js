/* eslint-disable camelcase */

import { mapState, mapActions } from 'vuex';

import { logIn, logOut } from '../utils/auth-actions';
import tokenUserMixin from './token-user';
import { TITLE_SUFFIX } from '../constants';
import { InvalidRouteError } from '../errors';

export default {
  mixins: [tokenUserMixin],

  props: {
    parentIsFetching: {
      type: Boolean,
      required: true,
    },
  },

  data() {
    return { isFetching: true };
  },

  async created() {
    const { isProtected, isExact } = this.route;
    const { email_verified } = this.tokenUser;
    const { accessToken, parentIsFetching } = this;

    if (isExact) this.setTitle();

    if (!accessToken && isProtected) {
      logIn();
    } else if (!email_verified && isProtected) {
      this.setUnverified();
    } else if (!parentIsFetching) {
      await this.doRoutePrepare();
    }
  },

  computed: {
    ...mapState('tokenUser', ['accessToken']),
  },

  methods: {
    ...mapActions('context', ['setUnverified', 'setError']),

    setTitle() {
      document.title = `${this.route.title} ${TITLE_SUFFIX}`;
    },

    logPageView() {
      window.dataLayer.push({
        event: 'userPortalPageview',
        pagePath: window.location.pathname,
        pageTitle: document.title,
      });
    },

    async doRoutePrepare() {
      const { isExact } = this.route;

      try {
        await this.prepareRoute();
        if (isExact) this.logPageView();
        this.isFetching = false;
      } catch (err) {
        if (err instanceof InvalidRouteError) {
          this.$router.push({ name: 'home' });
        } else {
          this.setError(err);
        }
      }
    },
  },

  watch: {
    accessToken(newToken, oldToken) {
      const {
        route: { isProtected },
      } = this;

      if (isProtected && oldToken && !newToken) logOut();
    },

    async parentIsFetching() {
      await this.doRoutePrepare();
    },
  },
};
