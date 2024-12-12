/* eslint-disable no-underscore-dangle */
import Vue from 'vue';
import VueRouter from 'vue-router';

import RouteHandler from '../../RouteHandler.vue';
import TopForm from './TopForm.vue';
import mergeValuesIntoStartState from '../../utils/merge-values-into-start-state';
import sanitizeParams from '../../utils/sanitize-params';
import { BLAST_LEVELS, BLAST_FORM_STATE, DEFAULT_LEVEL } from './constants';

Vue.use(VueRouter);

function getStateFromParams(queryParams) {
  const cleanParams = sanitizeParams(queryParams);
  let { level = "" } = cleanParams;
  const {
    campaignId = '',
    referralId = '',
    firstName = '',
    lastName = '',
    email = '',
    zipcode = '',
  } = cleanParams;

  if (!BLAST_LEVELS[level]) level = DEFAULT_LEVEL;

  const { amount, installmentPeriod } = BLAST_LEVELS[level];

  return {
    level,
    amount,
    zipcode,
    first_name: firstName,
    last_name: lastName,
    stripeEmail: email,
    installment_period: installmentPeriod,
    campaign_id: campaignId,
    referral_id: referralId,
  };
}

function createInitialFormState(queryParams) {
  // if form submission was invalid,
  // rehydrate the store from the JSON blob in the template
  if (window.__BLAST_FORM_REHYDRATION__) {
    return mergeValuesIntoStartState(
      BLAST_FORM_STATE,
      window.__BLAST_FORM_REHYDRATION__
    );
  }

  const paramState = getStateFromParams(queryParams);
  // merge query-parameter values into full state object,
  // which contains validation information
  return mergeValuesIntoStartState(BLAST_FORM_STATE, paramState);
}

function createRouter() {
  return new VueRouter({
    base: '/blast',
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
      'blastForm/createInitialState',
      createInitialFormState(query)
    );

    routeHandler.$mount('#app');
    topForm.$mount('#blast-form');
  });
}

export { createRouter, bindRouterEvents };
