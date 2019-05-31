import Vue from 'vue';
import VueRouter from 'vue-router';

import App from './App.vue';
import routes from './routes';
import store from './store';
import SiteFooter from './components/SiteFooter.vue';
import NavBar from './components/NavBar.vue';
import Icon from './components/Icon.vue';
import { Auth0Error } from './errors';

Vue.use(VueRouter);
Vue.component('SiteFooter', SiteFooter);
Vue.component('NavBar', NavBar);
Vue.component('Icon', Icon);

store
  .dispatch('user/getUser')
  .catch(err => {
    if (err instanceof Auth0Error) {
      this.context.setError(true);
    }
  })
  .then(() => {
    const router = new VueRouter({
      base: '/user-portal',
      mode: 'history',
      routes,
      scrollBehavior: () => ({ x: 0, y: 0 }),
    });

    router.beforeEach((to, from, next) => {
      store.dispatch('context/setIsFetching', true);
      next();
    });

    router.afterEach(() => {
      store.dispatch('context/setIsFetching', false);
    });

    const instance = new Vue({ ...App, router, store });
    instance.$mount('#user-portal-attach');
  });
