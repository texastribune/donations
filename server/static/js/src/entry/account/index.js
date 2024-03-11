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
import { init as initSentry } from '@sentry/browser';
import getYear from 'date-fns/get_year';

import routes from './routes';
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
import setTitle from './utils/set-title';
import logPageView from './utils/log-page-view';

import { UnverifiedError, AxiosError } from './errors';
import {
  SENTRY_DSN,
  SENTRY_ENVIRONMENT,
  ENABLE_SENTRY,
  GA_USER_PORTAL_NAV,
  GA_USER_PORTAL,
  GA_DONATIONS,
  GA_BLAST_INTENT,
  GA_CUSTOM_EVENT_NAME,
  DONATE_URL,
  CIRCLE_URL,
} from './constants';
import {
  CONTEXT_TYPES,
  CONTEXT_MODULE,
  TOKEN_USER_TYPES,
  TOKEN_USER_MODULE,
} from './store/types';

if (ENABLE_SENTRY) {
  initSentry({
    dsn: SENTRY_DSN,
    environment: SENTRY_ENVIRONMENT,
    integrations: [new VueIntegration({ Vue })],
  });
}

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
      urls: {
        donate: DONATE_URL,
        circle: CIRCLE_URL,
      },
      dates: {
        lastYear: getYear(new Date()) - 1,
        thisYear: getYear(new Date()),
      },
    };
  },
});

Vue.use(VModal);
Vue.use(VueRouter);
Vue.use(VueClipboard);

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
    const { code, response, message } = error;
    const errorDetail = { message, extra: {} };

    if (response) {
      const { data, status } = response;
      errorDetail.status = status;
      errorDetail.extra.data = data;
      errorDetail.extra.gotResponse = true;
    } else {
      errorDetail.extra.gotResponse = false;
    }

    if (code) {
      errorDetail.extra.code = code;
    }

    return Promise.reject(new AxiosError(errorDetail));
  }
);

axios.interceptors.request.use(
  config => config,
  error => Promise.reject(new AxiosError({ message: error.message }))
);

function getInterval() {
  const tokenExpiryInMs = store.getters[`${TOKEN_USER_MODULE}/tokenExpiryInMs`];
  const nowInMs = Date.now();
  const fiveMinutesInMs = 5 * 60 * 1000;

  return tokenExpiryInMs - nowInMs - fiveMinutesInMs;
}

function refreshTokens() {
  setTimeout(async () => {
    await store.dispatch(
      `${TOKEN_USER_MODULE}/${TOKEN_USER_TYPES.getTokenUser}`
    );

    const isReady = store.getters[`${TOKEN_USER_MODULE}/isReady`];

    if (isReady) {
      refreshTokens();
    }
  }, getInterval());
}

store
  .dispatch(`${TOKEN_USER_MODULE}/${TOKEN_USER_TYPES.getTokenUser}`)
  .then(() => {
    const isReady = store.getters[`${TOKEN_USER_MODULE}/isReady`];
    const router = new VueRouter({
      base: '/account',
      mode: 'history',
      routes,
      scrollBehavior(to, from, savedPosition) {
        if (savedPosition) {
          return savedPosition;
        }
        return { x: 0, y: 0 };
      },
    });

    if (isReady) {
      refreshTokens();
    }

    router.onError(err => {
      store.dispatch(`${CONTEXT_MODULE}/${CONTEXT_TYPES.setError}`, err);
      store.dispatch(`${CONTEXT_MODULE}/${CONTEXT_TYPES.setIsFetching}`, false);

      if (!(err instanceof UnverifiedError)) {
        logError({ err });
      }
    });

    router.beforeEach(async (to, from, next) => {
      store.dispatch(`${CONTEXT_MODULE}/${CONTEXT_TYPES.setIsFetching}`, true);

      const isVerified = store.getters[`${TOKEN_USER_MODULE}/isVerified`];
      const { isLoggedIn, error: tokenUserError } = store.state[
        TOKEN_USER_MODULE
      ];

      if (to.meta.isProtected) {
        if (!isLoggedIn) {
          return logIn();
        }

        if (tokenUserError) {
          return next(tokenUserError);
        }

        if (!isVerified) {
          return next(new UnverifiedError());
        }
      }

      let diffed = false;
      const activated = to.matched.filter(
        // eslint-disable-next-line no-return-assign
        (route, i) => diffed || (diffed = from.matched[i] !== route)
      );
      const fetchers = activated
        .map(route => route.meta.fetchData)
        .filter(fetcher => !!fetcher);

      try {
        if (to.meta.requiresParentFetch) {
          // eslint-disable-next-line no-restricted-syntax
          for (const fetcher of fetchers) {
            // eslint-disable-next-line no-await-in-loop
            await fetcher(to, from);
          }
        } else {
          await Promise.all(fetchers.map(fetcher => fetcher(to, from)));
        }
      } catch (err) {
        return next(err);
      }

      return next();
    });

    router.afterEach(to => {
      const { error: appError } = store.state[CONTEXT_MODULE];

      if (!appError) {
        setTitle(to.meta.title);

        Vue.nextTick(() => {
          logPageView();
        });
      }

      store.dispatch(`${CONTEXT_MODULE}/${CONTEXT_TYPES.setIsFetching}`, false);
    });

    new Vue({ ...App, router, store }).$mount('#account-attach');
  });
