import Vue from 'vue';
import Vuex from 'vuex';
import VueRouter from 'vue-router';

import App from './App.vue';
import routes from './routes';
import userModule from './store/modules/user';
import contextModule from './store/modules/context';

Vue.use(Vuex);
Vue.use(VueRouter);

const router = new VueRouter({
  base: '/user-portal',
  mode: 'history',
  routes,
});
const store = new Vuex.Store({
  modules: {
    user: userModule,
    context: contextModule,
  },
});
const instance = new Vue({ ...App, router, store });

instance.$mount('#user-portal-attach');
