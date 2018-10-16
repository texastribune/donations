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
  DEFAULT_DONATION_LEVEL_WITH_INSTALL_PERIOD,
  DEFAULT_ONCE_DONATION_LEVEL_WITH_INSTALL_PERIOD,
  LONG_PROGRAM_NAME,
  WL_DEFAULT_QUERY_PARAMETERS,
  WL_QUERY_ESCAPE_THRESHOLD,
  QUERY_PARAMETERS_STRING_VALUES,
} from './constants';

Vue.use(VueRouter);


function getStateFromParams(queryParams) {
  let scrubbedQueryParams;
  //console.log("wl def object");
  //console.log(WL_DEFAULT_QUERY_PARAMETERS);
  //
  // If this query is within the threshold number of parameters
  //   scrub and merge query params with the default state
  // Otherwise, it's likely to be malicious,
  //   ignore query params and use defaults
  //
  (Object.keys(queryParams).length <= WL_QUERY_ESCAPE_THRESHOLD) ?
    scrubbedQueryParams = queryParamScrubAndMerge(queryParams, Object.keys(WL_DEFAULT_QUERY_PARAMETERS)) :
    scrubbedQueryParams = {};
  //
  // Result is parameters merged from defaults and query parameter overrides
  //
  const mergedQueryParams = Object.assign({}, WL_DEFAULT_QUERY_PARAMETERS, scrubbedQueryParams);

  let level = DEFAULT_DONATION_LEVEL_WITH_INSTALL_PERIOD;
  // Unpack and interpret query params per spec
  if (mergedQueryParams.installmentPeriod.toLowerCase() === QUERY_PARAMETERS_STRING_VALUES.onceStr) {
    // Set data for form submit
    mergedQueryParams.installments = QUERY_PARAMETERS_STRING_VALUES.oneStr;
    mergedQueryParams.installment_period = QUERY_PARAMETERS_STRING_VALUES.noneStr;
    mergedQueryParams.openended_status = QUERY_PARAMETERS_STRING_VALUES.noneStr;
    // Set UI
    level = DEFAULT_ONCE_DONATION_LEVEL_WITH_INSTALL_PERIOD;
  }
  //console.log("form start");
  //console.log(mergedQueryParams);
  // Set the Choices form state from defaults + query parameters
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

function createInitialFormState(queryParams) {
  if (window.__BUSINESS_FORM_REHYDRATION__) {
    return window.__BUSINESS_FORM_REHYDRATION__;
  }
  const dynamicState = getStateFromParams(queryParams);
  const staticState = {
    stripeEmail: '',
    customerId: '',
    business_name: '',
    website: '',
    shipping_street: '',
    shipping_city: '',
    shipping_state: '',
    shipping_postalcode: '',
    first_name: '',
    last_name: '',
    description: LONG_PROGRAM_NAME,
    reason: '',
    pay_fees_value: DEFAULT_PAY_FEES,
  };

  return { ...staticState, ...dynamicState };
}

function createRouter() {
  return new VueRouter({
    base: '/business',
    mode: 'history',
    routes: [
      { path: '/', component: RouteHandler },
    ],
  });
}

function bindRouterEvents(router, routeHandler, store) {
  router.onReady(() => {
    const topForm = new Vue({ ...BusinessForm, store });

    const { currentRoute: { query } } = router;

    store.dispatch(
      'businessForm/createInitialState',
      createInitialFormState(query),
    );

    routeHandler.$mount('#app');
    topForm.$mount('#business-form');
    // wall.$mount('#business-wall');
  });
}

export { createRouter, bindRouterEvents };

// Test strings
//  http://local.texastribune.org/businessform?installmentPeriod=once
//  http://local.texastribune.org/businessform?campaignId=ui903&installmentPeriod=once
//  http://local.texastribune.org/businessform?campaignId=ui903&installmentPeriod=once&foo=bar
//  http://local.texastribune.org/businessform?campaignId=ui903&installmentPeriod=once&<script>jk//∫ß
