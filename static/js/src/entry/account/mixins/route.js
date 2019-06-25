/* eslint-disable camelcase */

import { mapState, mapActions } from 'vuex';

import { logIn, logOut } from '../utils/auth-actions';
import tokenUserMixin from './token-user';
import { TITLE_SUFFIX } from '../constants';

export default {
  mixins: [tokenUserMixin],

  data() {
    return { isFetching: !!this.$options.methods.fetchData };
  },

  async created() {
    const { isProtected, isExact, meetsCriteria } = this.route;
    const { email_verified } = this.tokenUser;
    const { accessToken } = this;

    if (isExact) this.setTitle();

    if (!accessToken && isProtected) {
      logIn();
    } else if (!email_verified && isProtected) {
      this.setUnverified();
    } else if (!meetsCriteria) {
      this.$router.push({ name: 'home' });
    } else if (this.fetchData) {
      try {
        await this.fetchData();
        if (isExact) this.logPageView();
        this.isFetching = false;
      } catch (err) {
        this.setError(err);
      }
    } else if (isExact) {
      this.logPageView();
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
  },

  watch: {
    accessToken(newToken, oldToken) {
      const {
        route: { isProtected },
      } = this;

      if (isProtected && oldToken && !newToken) logOut();
    },
  },
};
