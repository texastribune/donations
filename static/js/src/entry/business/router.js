import Vue from 'vue';
import VueRouter from 'vue-router';

import RouteHandler from '../../RouteHandler.vue';
import BusinessForm from './BusinessForm.vue';

import queryParamScrubAndMerge from '../../utils/queryParameterHandlers';
// Temp out V2 add
// import Wall from './Wall.vue';

import {
  BUSINESS_BUCKETS,
  DEFAULT_PAY_FEES,
  DEFAULT_DONATION_LEVEL,
  LONG_PROGRAM_NAME,
  WL_DEFAULT_QUERY_PARAMETERS,
  WL_QUERY_ESCAPE_THRESHOLD,
  QUERY_PARAMETERS_STRING_VALUES,
} from './constants';

Vue.use(VueRouter);


function getStateFromParams(queryParams) {
  const defaultLevel = DEFAULT_DONATION_LEVEL;
  let scrubbedQueryParams;
  //
  // If this query significantly exceeds the threshold number of parameters
  // it's likely to be malicious,ignore query params and use defaults
  // in this case
  //
  (Object.keys(queryParams).length <= WL_QUERY_ESCAPE_THRESHOLD) ?
    scrubbedQueryParams = queryParamScrubAndMerge(queryParams, Object.keys(WL_DEFAULT_QUERY_PARAMETERS)) :
    scrubbedQueryParams = {};
  //
  // Result is parameters merged from defaults and query parameter overrides
  //
  const mergedQueryParams = Object.assign({}, WL_DEFAULT_QUERY_PARAMETERS, scrubbedQueryParams);

  // Unpack and interpret query params per spec and add them to query vars
  if (mergedQueryParams.installmentPeriod.toLowerCase() === QUERY_PARAMETERS_STRING_VALUES.onceStr) {
    mergedQueryParams.installments = QUERY_PARAMETERS_STRING_VALUES.oneStr;
    mergedQueryParams.installment_period = QUERY_PARAMETERS_STRING_VALUES.noneStr;
    mergedQueryParams.openended_status = QUERY_PARAMETERS_STRING_VALUES.noneStr;
  }

  console.log('>>>>>>>>>>>>>--------- merged and split query params ->');
  console.log(mergedQueryParams);

  const level = defaultLevel;
  const {
    amount,
    payFees,
  } = BUSINESS_BUCKETS[level];

  return {
    level,
    amount,
    pay_fees_value: payFees,
    campaign_id: mergedQueryParams.campaignId,
    referral_id: mergedQueryParams.referralId,
    installment_period: mergedQueryParams.installment_period,
    installments: mergedQueryParams.installments,
    openended_status: mergedQueryParams.openended_status,
  };
}

function createBaseFormState(queryParams) {
  const dynamicState = getStateFromParams(queryParams);
  const staticState = {
    stripeEmail: '',
    customerId: '',
    first_name: '',
    last_name: '',
    description: LONG_PROGRAM_NAME,
    reason: '',
    zipcode: '',
    pay_fees_value: DEFAULT_PAY_FEES,
  };

  return { ...staticState, ...dynamicState };
}

function createRouter() {
  return new VueRouter({
    base: '/businessform',
    mode: 'history',
    routes: [
      { path: '/', component: RouteHandler },
    ],
  });
}

function bindRouterEvents(router, routeHandler, store) {
  router.onReady(() => {
    const topForm = new Vue({ ...BusinessForm, store });
    // const wall = new Vue({ ...Wall });
    const { currentRoute: { query } } = router;

    store.dispatch(
      'businessForm/createInitialState',
      createBaseFormState(query),
    );

    routeHandler.$mount('#app');
    topForm.$mount('#business-form');
    // wall.$mount('#business-wall');
  });
}

export { createRouter, bindRouterEvents };
