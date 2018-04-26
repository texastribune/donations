import Vue from 'vue';
import VueRouter from 'vue-router';
import Vuex from 'vuex';

import App from '../App.vue';
import DonateForm from '../containers/DonateForm.vue';
import FormModule from '../store/modules/form';

Vue.use(VueRouter);
Vue.use(Vuex);

const router = new VueRouter({
  base: '/devdonate',
  mode: 'history',
  routes: [
    { path: '/', component: DonateForm },
  ],
});

const store = new Vuex.Store({
  modules: {
    form: FormModule,
  },
});

const app = new Vue({ ...App, router, store });

router.onReady(() => {
  const { currentRoute } = router;
  store.dispatch('form/createInitialState', { amount: currentRoute.query.amount });
  app.$mount('#app');
});
