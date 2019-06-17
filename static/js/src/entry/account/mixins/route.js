import { TITLE_SUFFIX } from '../constants';

export default {
  mounted() {
    if (!this.unauthorizedFetch) {
      this.setTitle();
      this.logPageView();
    }
  },

  methods: {
    setTitle() {
      document.title = `${this.$route.meta.title} ${TITLE_SUFFIX}`;
    },

    logPageView() {
      window.dataLayer.push({
        event: 'userPortalPageview',
        pagePath: window.location.pathname,
        pageTitle: document.title,
      });
    },
  },
};
