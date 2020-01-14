import Vue from 'vue';
import VueRouter from 'vue-router';
import VModal from 'vue-js-modal';
import { extend as extendValidationRule } from 'vee-validate';
import {
  required as requiredRule,
  email as emailRule,
  numeric as numericRule,
} from 'vee-validate/dist/rules';
import VueClipboard from 'vue-clipboard2';
import axios from 'axios';
import { Vue as VueIntegration } from '@sentry/integrations';
import { init as initSentry, setExtra } from '@sentry/browser';

import routes from './routes'; // eslint-disable-line
import store from './store';
import App from './App.vue';
import UserSiteFooter from './nav/components/UserSiteFooter.vue';
import BasicSiteFooter from './nav/components/BasicSiteFooter.vue';
import UserNavBar from './nav/components/UserNavBar.vue';
import BasicNavBar from './nav/components/BasicNavBar.vue';
import UserInternalNav from './nav/components/UserInternalNav.vue';
import Icon from './components/Icon.vue';
import BaseButton from './components/BaseButton.vue';
import formatCurrency from './utils/format-currency';
import formatLongDate from './utils/format-long-date';
import formatShortDate from './utils/format-short-date';
import { logIn } from './utils/auth-actions';
import logError from './utils/log-error';
import { UnverifiedError, AxiosError } from './errors';
import {
  SENTRY_DSN,
  SENTRY_ENVIRONMENT,
  ENABLE_SENTRY,
  GA_USER_PORTAL_NAV,
  GA_USER_PORTAL,
  GA_DONATIONS,
  GA_BLAST_INTENT,
  GA_TRIBUNE_AMBASSADORS,
  GA_AMBASSADORS_CUSTOM_EVENT_NAME,
  GA_CUSTOM_EVENT_NAME,
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

Vue.use(VModal);
Vue.use(VueRouter);
Vue.use(VueClipboard);
Vue.mixin({
  data() {
    return {
      ga: {
        userPortal: GA_USER_PORTAL,
        userPortalNav: GA_USER_PORTAL_NAV,
        donations: GA_DONATIONS,
        blastIntent: GA_BLAST_INTENT,
        tribuneAmbassadors: GA_TRIBUNE_AMBASSADORS,
        customEventName: GA_CUSTOM_EVENT_NAME,
        ambassadorsCustomEventName: GA_AMBASSADORS_CUSTOM_EVENT_NAME,
      },
      donateUrl: DONATE_URL,
      circleUrl: CIRCLE_URL,
    };
  },
});

Vue.component('UserSiteFooter', UserSiteFooter);
Vue.component('BasicSiteFooter', BasicSiteFooter);
Vue.component('UserNavBar', UserNavBar);
Vue.component('BasicNavBar', BasicNavBar);
Vue.component('UserInternalNav', UserInternalNav);
Vue.component('Icon', Icon);
Vue.component('BaseButton', BaseButton);

Vue.filter('currency', formatCurrency);
Vue.filter('shortDate', formatShortDate);
Vue.filter('longDate', formatLongDate);

extendValidationRule('email', emailRule);
extendValidationRule('required', requiredRule);
extendValidationRule('numeric', numericRule);
extendValidationRule('confirm', {
  params: ['target'],

  validate(value, { target }) {
    return value === target;
  },
});

axios.interceptors.response.use(
  response => response,
  error => {
    setExtra('lastAxiosResponse', error.toJSON());
    return Promise.reject(new AxiosError());
  }
);

axios.interceptors.request.use(
  config => config,
  error => {
    setExtra('lastAxiosRequest', error.toJSON());
    return Promise.reject(new AxiosError());
  }
);

// we refresh at a 15-minute interval instead of when
// the access token expires because we want to regularly
// check whether a user has logged out of Auth0 in another app
function refreshToken() {
  setTimeout(async () => {
    await store.dispatch('tokenUser/getTokenUser');
    const isLoggedIn = store.getters['tokenUser/isLoggedIn'];
    if (isLoggedIn) refreshToken();
  }, 15 * 60 * 1000); // 15 minutes
}

store.dispatch('tokenUser/getTokenUser').then(() => {
  const router = new VueRouter({
    base: '/account',
    mode: 'history',
    routes,
    scrollBehavior: () => ({ x: 0, y: 0 }),
  });
  const isLoggedIn = store.getters['tokenUser/isLoggedIn'];

  if (isLoggedIn) {
    refreshToken();
  }

  router.beforeEach((to, from, next) => {
    store.dispatch('context/setIsFetching', true);

    const { isVerified, error: tokenUserError } = store.state.tokenUser;
    // eslint-disable-next-line no-shadow
    const isLoggedIn = store.getters['tokenUser/isLoggedIn'];

    if (to.meta.isProtected) {
      if (tokenUserError) {
        logError(tokenUserError);
        store.dispatch('context/setError', tokenUserError);
        return next();
      }

      if (!isLoggedIn) {
        return logIn();
      }

      if (!isVerified) {
        store.dispatch('context/setError', new UnverifiedError());
        return next();
      }
    }

    return next();
  });

  router.afterEach(() => {
    store.dispatch('context/setIsFetching', false);
  });

  const instance = new Vue({ ...App, router, store });
  instance.$mount('#account-attach');
});
