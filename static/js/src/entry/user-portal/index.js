import Vue from 'vue';
import Vuex from 'vuex';
import VueRouter from 'vue-router';

import Portal from './Portal.vue';
import routes from './routes';
import userModule from '../../store/modules/user';

import './styles.scss';

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
  },
});
const instance = new Vue({ ...Portal, router, store });

instance.$mount('#user-portal-attach');
