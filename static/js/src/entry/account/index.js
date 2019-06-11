import Vue from 'vue';
import VueRouter from 'vue-router';
import addSeconds from 'date-fns/add_seconds';
import subtractMinutes from 'date-fns/sub_minutes';
import differenceInMilliSeconds from 'date-fns/difference_in_milliseconds';

import App from './App.vue';
import routes from './routes';
import store from './store';
import SiteFooter from './containers/SiteFooterContainer.vue';
import Loader from './components/Loader.vue';
import NavBar from './containers/NavBarContainer.vue';
import Icon from './components/Icon.vue';
import { LoggedOutError } from './errors';

Vue.use(VueRouter);
Vue.component('SiteFooter', SiteFooter);
Vue.component('NavBar', NavBar);
Vue.component('Loader', Loader);
Vue.component('Icon', Icon);

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
      await store.dispatch('user/getTokenUser');
      const newRefreshAt = getRefreshInterval(store.state.user.expiryInSeconds);
      refreshToken(newRefreshAt);
    } catch (err) {
      if (!(err instanceof LoggedOutError)) {
        store.dispatch('context/setError', true);
      }
    }
  }, refreshAt);
}

store
  .dispatch('user/getTokenUser')
  .catch(err => {
    if (!(err instanceof LoggedOutError)) {
      store.dispatch('context/setError', true);
    }
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

    const refreshAt = getRefreshInterval(store.state.user.expiryInSeconds);
    refreshToken(refreshAt);
  });
