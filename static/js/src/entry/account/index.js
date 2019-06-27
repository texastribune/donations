/* eslint-disable import/first */

import Vue from 'vue';
import { init as initSentry } from '@sentry/browser';
import { Vue as VueIntegration } from '@sentry/integrations';
import VueRouter from 'vue-router';
import addSeconds from 'date-fns/add_seconds';
import subtractMinutes from 'date-fns/sub_minutes';
import differenceInMilliSeconds from 'date-fns/difference_in_milliseconds';

import {
  SENTRY_DSN,
  SENTRY_ENVIRONMENT,
  ENABLE_SENTRY,
  GA_USER_PORTAL_NAV,
  GA_USER_PORTAL,
  GA_DONATIONS,
  GA_CUSTOM_EVENT_NAME,
  GA_BLAST_INTENT,
  DONATE_URL,
  CIRCLE_URL,
} from './constants';

if (ENABLE_SENTRY) {
  initSentry({
    dsn: SENTRY_DSN,
    environment: SENTRY_ENVIRONMENT,
    integrations: [new VueIntegration({ Vue })],
  });
}

import App from './App.vue';
import routes from './routes'; // eslint-disable-line
import store from './store';
import SiteFooter from './containers/SiteFooterContainer.vue';
import Loader from './components/Loader.vue';
import NavBar from './containers/NavBarContainer.vue';
import Icon from './components/Icon.vue';
import formatCurrency from './utils/format-currency';
import formatLongDate from './utils/format-long-date';
import formatShortDate from './utils/format-short-date';
import logError from './utils/log-error';

Vue.use(VueRouter);

Vue.mixin({
  data() {
    return {
      ga: {
        userPortal: GA_USER_PORTAL,
        userPortalNav: GA_USER_PORTAL_NAV,
        donations: GA_DONATIONS,
        blastIntent: GA_BLAST_INTENT,
        customEventName: GA_CUSTOM_EVENT_NAME,
      },
      donateUrl: DONATE_URL,
      circleUrl: CIRCLE_URL,
    };
  },

  methods: {
    logError(err, level) {
      logError(err, level);
    },
  },
});

Vue.component('SiteFooter', SiteFooter);
Vue.component('NavBar', NavBar);
Vue.component('Loader', Loader);
Vue.component('Icon', Icon);

Vue.filter('currency', formatCurrency);
Vue.filter('shortDate', formatShortDate);
Vue.filter('longDate', formatLongDate);

// https://itnext.io/managing-and-refreshing-auth0-tokens-in-a-vuejs-application-65eb29c309bc
function getRefreshInterval(expiryInSeconds) {
  const tokenExpiryDate = addSeconds(new Date(), expiryInSeconds);
  const tenMinutesBeforeExpiry = subtractMinutes(tokenExpiryDate, 10);
  const now = new Date();
  const interval = differenceInMilliSeconds(tenMinutesBeforeExpiry, now);

  return interval;
}

function refreshToken(refreshAt) {
  setTimeout(async () => {
    try {
      await store.dispatch('tokenUser/getTokenUser');
      const newRefreshAt = getRefreshInterval(store.state.user.expiryInSeconds);
      refreshToken(newRefreshAt);
    } catch (err) {
      store.dispatch('context/setError', err);
    }
  }, refreshAt);
}

store
  .dispatch('tokenUser/getTokenUser')
  .catch(err => {
    store.dispatch('context/setError', err);
  })
  .then(() => {
    const router = new VueRouter({
      base: '/account',
      mode: 'history',
      routes,
      scrollBehavior: () => ({ x: 0, y: 0 }),
    });

    const instance = new Vue({ ...App, router, store });
    instance.$mount('#account-attach');

    const { expiryInSeconds, accessToken } = store.state.tokenUser;

    if (accessToken) {
      const refreshAt = getRefreshInterval(expiryInSeconds);
      refreshToken(refreshAt);
    }
  });
