import Vue from 'vue';
import VueRouter from 'vue-router';

import RouteHandler from '../../RouteHandler.vue';
import BusinessForm from './BusinessForm.vue';
// Temp out V2 add
// import Wall from './Wall.vue';

import {
  BUSINESS_BUCKETS,
  DEFAULT_PAY_FEES,
  DEFAULT_DONATION_LEVEL,
  LONG_PROGRAM_NAME,
  WL_DEFAULT_QUERY_PARAMETERS,
  WL_QUERY_ESCAPE_THRESHOLD,
} from './constants';

Vue.use(VueRouter);
//
// Query parameters
// ?campaign_id=
// ?referral_id=
// ?installments=
// ?openended_status=
// ?installment_period=
//
function queryParamScrubAndMerge(data, whitelist) {
  // Only process whitelisted parameters; for dupes the last value will bethe one used
  return whitelist.reduce((result, key) =>
    (data[key] !== undefined
      ? Object.assign(result, { [key]: data[key] })
      : result), {});
}

function getStateFromParams(queryParams) {
  const defaultLevel = DEFAULT_DONATION_LEVEL;
  let scrubbedQueryParams;
  //
  // If this query significantly exceeds the threshold number of parameters it's likely to be malicious,
  // ignore query params and use defaults in this case
  //
  (Object.keys(queryParams).length <= WL_QUERY_ESCAPE_THRESHOLD) ?
    scrubbedQueryParams = queryParamScrubAndMerge(queryParams, Object.keys(WL_DEFAULT_QUERY_PARAMETERS)) :
    scrubbedQueryParams = {};

  // Create whitelist to filter out any bogus query params
  const mergedQueryParams = Object.assign({}, WL_DEFAULT_QUERY_PARAMETERS, scrubbedQueryParams);

  console.log('>>>>>>>>>>>>>--------- mergedQueryParams ->');
  console.log(mergedQueryParams);

  const level = defaultLevel;
  const {
    amount,
    payFees,
  } = BUSINESS_BUCKETS[level];

  return {
    level,
    amount,
    installments: scrubbedQueryParams.installments,
    openended_status: scrubbedQueryParams.openended_status,
    pay_fees_value: payFees,
    installment_period: scrubbedQueryParams.installment_period,
    campaign_id: scrubbedQueryParams.campaign_id,
    referral_id: scrubbedQueryParams.referral_id,
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
    openended_status: 'None',
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
