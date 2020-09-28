/* eslint-disable no-underscore-dangle */
import Vue from 'vue';
import VueRouter from 'vue-router';

import RouteHandler from '../../RouteHandler.vue';
import TopForm from './TopForm.vue';
import mergeValuesIntoStartState from '../../utils/merge-values-into-start-state';
import sanitizeParams from '../../utils/sanitize-params';
import { BASE_FORM_STATE, AMBASSADOR_CODES } from './constants';

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

  const cleanParams = sanitizeParams(queryParams);
  const {
    campaignId = '',
    referralId = '',
    firstName = '',
    lastName = '',
    email = '',
    zipcode = '',
    code = '',
  } = cleanParams;
  let amount;
  let installmentPeriod;

  if (code && AMBASSADOR_CODES[code]) {
    ({ amount, installmentPeriod } = AMBASSADOR_CODES[code]);
  } else {
    ({ amount, installmentPeriod = 'monthly' } = cleanParams);

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
  }

  // merge query-parameter values into full state object,
  // which contains validation information
  return mergeValuesIntoStartState(BASE_FORM_STATE, {
    amount,
    zipcode,
    first_name: firstName,
    last_name: lastName,
    stripeEmail: email,
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
