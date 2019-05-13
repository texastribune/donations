/* eslint-disable no-underscore-dangle */
import Vue from 'vue';
import VueRouter from 'vue-router';

import RouteHandler from '../../RouteHandler.vue';
import TopForm from './TopForm.vue';
import mergeValuesIntoStartState from '../../utils/mergeValuesIntoStartState';
import { BASE_FORM_STATE } from './constants';

Vue.use(VueRouter);

function createInitialFormState(queryParams) {
  // if form submission was invalid,
  // rehydrate the store from the JSON blob in the template
  if (window.__BASE_FORM_REHYDRATION__) {
    return mergeValuesIntoStartState(
      BASE_FORM_STATE,
      window.__BASE_FORM_REHYDRATION__
    );
  }

  let { amount, installmentPeriod = 'monthly' } = queryParams;
  const { campaignId = '', referralId = '' } = queryParams;

  switch (installmentPeriod.toLowerCase()) {
    case 'once':
      installmentPeriod = 'None';
      amount = amount || '60';
      break;
    case 'monthly':
      amount = amount || '35';
      break;
    case 'yearly':
      amount = amount || '75';
      break;
    default:
      installmentPeriod = 'monthly';
      amount = amount || '35';
  }

  // merge query-parameter values into full state object,
  // which contains validation information
  return mergeValuesIntoStartState(BASE_FORM_STATE, {
    amount,
    campaign_id: campaignId,
    referral_id: referralId,
    installment_period: installmentPeriod,
  });
}

function createRouter() {
  return new VueRouter({
    base: '/donate',
    mode: 'history',
    routes: [{ path: '/', component: RouteHandler }],
  });
}

function bindRouterEvents(router, routeHandler, store) {
  router.onReady(() => {
    const topForm = new Vue({ ...TopForm, store });
    const {
      currentRoute: { query },
    } = router;

    store.dispatch(
      'baseForm/createInitialState',
      createInitialFormState(query)
    );

    routeHandler.$mount('#app');
    topForm.$mount('#top-form');
  });
}

export { createRouter, bindRouterEvents };
