import Vue from 'vue';
import VueRouter from 'vue-router';
import Vuex from 'vuex';

import App from '../App.vue';
import Form from '../containers/Form.vue';

Vue.use(VueRouter);
Vue.use(Vuex);

const router = new VueRouter({
  base: '/devdonate',
  mode: 'history',
  routes: [
    { path: '/', component: Form },
  ],
});

/* eslint-disable no-new */
new Vue({
  el: '#app',
  components: { App },
  template: '<App/>',
  router,
  render: h => h(App),
});
