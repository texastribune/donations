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

function createInitialState(queryParams) {
  let openEndedStatus;
  let { amount, installmentPeriod = 'monthly' } = queryParams;
  const { campaignId = '' } = queryParams;

  switch (installmentPeriod.toLowerCase()) {
    case 'monthly':
      openEndedStatus = 'Open';
      amount = amount || '10';
      break;
    case 'yearly':
      openEndedStatus = 'Open';
      amount = amount || '75';
      break;
    case 'once':
      openEndedStatus = 'None';
      installmentPeriod = 'None';
      amount = amount || '75';
      break;
    default:
      installmentPeriod = 'monthly';
      openEndedStatus = 'Open';
      amount = amount || '10';
  }

  return {
    amount,
    campaignId,
    installmentPeriod,
    openEndedStatus,
  };
}

router.onReady(() => {
  store.dispatch(
    'form/createInitialState',
    createInitialState(router.currentRoute.query),
  );
  app.$mount('#app');
});
