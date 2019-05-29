import Vue from 'vue';
import VueRouter from 'vue-router';

import App from './App.vue';
import routes from './routes';
import store from './store';
import SiteFooter from './components/SiteFooter.vue';
import Loader from './components/Loader.vue';

Vue.use(VueRouter);
Vue.component('SiteFooter', SiteFooter);
Vue.component('Loader', Loader);

const router = new VueRouter({
  base: '/user-portal',
  mode: 'history',
  routes,
  scrollBehavior: () => ({ x: 0, y: 0 }),
});
const instance = new Vue({ ...App, router, store });

instance.$mount('#user-portal-attach');
