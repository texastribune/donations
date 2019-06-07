import Vue from 'vue';
import VueRouter from 'vue-router';

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

store
  .dispatch('user/getTokenUser')
  .catch(err => {
    if (!(err instanceof LoggedOutError)) {
      store.dispatch('context/setError', true);
    }
  })
  .then(() => {
    const router = new VueRouter({
      base: '/user-portal',
      mode: 'history',
      routes,
      scrollBehavior: () => ({ x: 0, y: 0 }),
    });

    const instance = new Vue({ ...App, router, store });
    instance.$mount('#user-portal-attach');
  });
