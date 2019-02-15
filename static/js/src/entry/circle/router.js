/* eslint-disable no-underscore-dangle */
import Vue from 'vue';
import VueRouter from 'vue-router';

import RouteHandler from '../../RouteHandler.vue';
import TopForm from './TopForm.vue';
import Wall from './Wall.vue';
import mergeValuesIntoStartState from '../../utils/mergeValuesIntoStartState';
import { CIRCLE_BUCKETS, CIRCLE_FORM_STATE } from './constants';

Vue.use(VueRouter);

function getStateFromParams(queryParams) {
  const defaultLevel = 'editorMonthly';
  const { campaignId = '', referralId = '' } = queryParams;
  let { level = defaultLevel } = queryParams;

  if (!CIRCLE_BUCKETS[level]) level = defaultLevel;

  const { amount, installments, installmentPeriod } = CIRCLE_BUCKETS[level];

  return {
    level,
    amount,
    installments,
    installment_period: installmentPeriod,
    campaign_id: campaignId,
    referral_id: referralId,
  };
}

function createInitialFormState(queryParams) {
  // if form submission was invalid,
  // rehydrate the store from the JSON blob in the template
  if (window.__CIRCLE_FORM_REHYDRATION__) {
    return mergeValuesIntoStartState(
      CIRCLE_FORM_STATE,
      window.__CIRCLE_FORM_REHYDRATION__
    );
  }

  const paramState = getStateFromParams(queryParams);
  // merge query-parameter values into full state object,
  // which contains validation information
  return mergeValuesIntoStartState(CIRCLE_FORM_STATE, paramState);
}

function createRouter() {
  return new VueRouter({
    base: '/circle',
    mode: 'history',
    routes: [{ path: '/', component: RouteHandler }],
  });
}

function bindRouterEvents(router, routeHandler, store) {
  router.onReady(() => {
    const topForm = new Vue({ ...TopForm, store });
    const wall = new Vue({ ...Wall });
    const {
      currentRoute: { query },
    } = router;

    store.dispatch(
      'circleForm/createInitialState',
      createInitialFormState(query)
    );

    routeHandler.$mount('#app');
    topForm.$mount('#circle-form');
    wall.$mount('#circle-wall');
  });
}

export { createRouter, bindRouterEvents };
