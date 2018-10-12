/* eslint-disable no-underscore-dangle */
import Vue from 'vue';
import VueRouter from 'vue-router';

import RouteHandler from '../../RouteHandler.vue';
import TopForm from './TopForm.vue';

Vue.use(VueRouter);

function createInitialFormState(queryParams) {
  if (window.__BASE_FORM_REHYDRATION__) {
    return window.__BASE_FORM_REHYDRATION__;
  }

  const baseState = {
    stripeEmail: '',
    first_name: '',
    last_name: '',
    description: 'The Texas Tribune Membership',
    reason: '',
    zipcode: '',
    installments: 'None',
    pay_fees_value: 'False',
  };

  let openEndedStatus;
  let { amount, installmentPeriod = 'monthly' } = queryParams;
  const { campaignId = '', referralId = '' } = queryParams;

  switch (installmentPeriod.toLowerCase()) {
    case 'once':
      openEndedStatus = 'None';
      installmentPeriod = 'None';
      amount = amount || '60';
      break;
    case 'monthly':
      openEndedStatus = 'Open';
      amount = amount || '35';
      break;
    case 'yearly':
      openEndedStatus = 'Open';
      amount = amount || '75';
      break;
    default:
      installmentPeriod = 'monthly';
      openEndedStatus = 'Open';
      amount = amount || '35';
  }

  return {
    ...baseState,
    amount,
    campaign_id: campaignId,
    referral_id: referralId,
    installment_period: installmentPeriod,
    openended_status: openEndedStatus,
  };
}

function createRouter() {
  return new VueRouter({
    base: '/donate',
    mode: 'history',
    routes: [
      { path: '/', component: RouteHandler },
    ],
  });
}

function bindRouterEvents(router, routeHandler, store) {
  router.onReady(() => {
    const topForm = new Vue({ ...TopForm, store });
    const { currentRoute: { query } } = router;

    store.dispatch(
      'baseForm/createInitialState',
      createInitialFormState(query),
    );

    routeHandler.$mount('#app');
    topForm.$mount('#top-form');
  });
}

export { createRouter, bindRouterEvents };
