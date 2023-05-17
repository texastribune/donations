/* eslint-disable no-underscore-dangle, no-param-reassign */

import Vue from 'vue';
import VueRouter from 'vue-router';

import RouteHandler from '../../RouteHandler.vue';
import TopForm from './TopForm.vue';
import BusinessWall from './BusinessWall.vue';
import mergeValuesIntoStartState from '../../utils/merge-values-into-start-state';
import sanitizeParams from '../../utils/sanitize-params';
import {
  BUSINESS_LEVELS,
  BUSINESS_FORM_STATE,
  DEFAULT_LEVEL,
} from './constants';

Vue.use(VueRouter);

function getStateFromParams(queryParams) {
  const cleanParams = sanitizeParams(queryParams);
  const { campaignId = '', referralId = '' } = cleanParams;
  let { level = DEFAULT_LEVEL } = cleanParams;

  if (!BUSINESS_LEVELS[level]) level = DEFAULT_LEVEL;

  const { amount, installmentPeriod } = BUSINESS_LEVELS[level];

  return {
    level,
    amount,
    installment_period: installmentPeriod,
    campaign_id: campaignId,
    referral_id: referralId,
  };
}

function createInitialFormState(queryParams) {
  // if form submission was invalid,
  // rehydrate the store from the JSON blob in the template
  if (window.__BUSINESS_FORM_REHYDRATION__) {
    return mergeValuesIntoStartState(
      BUSINESS_FORM_STATE,
      window.__BUSINESS_FORM_REHYDRATION__
    );
  }

  const paramState = getStateFromParams(queryParams);
  // merge query-parameter values into full state object,
  // which contains validation information
  return mergeValuesIntoStartState(BUSINESS_FORM_STATE, paramState);
}

function createRouter() {
  return new VueRouter({
    base: '/business',
    mode: 'history',
    routes: [{ path: '/', component: RouteHandler }],
  });
}

function bindRouterEvents(router, routeHandler, store) {
  router.onReady(() => {
    const topForm = new Vue({ ...TopForm, store });
    const wall = new Vue({ ...BusinessWall });
    const {
      currentRoute: { query },
    } = router;

    store.dispatch(
      'businessForm/createInitialState',
      createInitialFormState(query)
    );

    routeHandler.$mount('#app');
    topForm.$mount('#business-form');
    wall.$mount('#business-wall');
  });
}

export { createRouter, bindRouterEvents };
