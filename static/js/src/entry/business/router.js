/* eslint-disable */
import Vue from 'vue';
import VueRouter from 'vue-router';

import RouteHandler from '../../RouteHandler.vue';
import BusinessForm from './BusinessForm.vue';

import queryParamWhiteListScrub from '../../utils/queryParameterHandlers';
// Temp out V2 add
// import Wall from './Wall.vue';

import {
  BUSINESS_BUCKETS,
  DEFAULT_PAY_FEES,
  DEFAULT_DONATION_LEVEL_WITH_INSTALL_PERIOD,
  DEFAULT_ONCE_DONATION_LEVEL_WITH_INSTALL_PERIOD,
  DEFAULT_STATE_SELECTED,
  LONG_PROGRAM_NAME,
  WL_DEFAULT_PARAMETERS,
  WL_QUERY_PARAMETERS_MAX_NBR_CHARS,
  WL_QUERY_ESCAPE_THRESHOLD,
  QUERY_PARAMETERS_STRING_VALUES,
} from './constants';

Vue.use(VueRouter);

function mapInstallmentPeriodOncetoForm(finalSanitizedParams) {
  // Set data for form submit
  finalSanitizedParams.installments = QUERY_PARAMETERS_STRING_VALUES.oneStr;
  finalSanitizedParams.installment_period =
    QUERY_PARAMETERS_STRING_VALUES.noneStr;
  finalSanitizedParams.openended_status =
    QUERY_PARAMETERS_STRING_VALUES.noneStr;
  return finalSanitizedParams;
}

function getStateFromParams(queryParams) {
  let level = DEFAULT_DONATION_LEVEL_WITH_INSTALL_PERIOD;
  //
  // If this query is within the threshold number of parameters
  //   filter input query oarams using the app whitelist
  //
  let scrubbedQueryParams;
  Object.keys(queryParams).length <= WL_QUERY_ESCAPE_THRESHOLD
    ? (scrubbedQueryParams = queryParamWhiteListScrub(
        queryParams,
        WL_DEFAULT_PARAMETERS,
        WL_QUERY_PARAMETERS_MAX_NBR_CHARS
      ))
    : (scrubbedQueryParams = WL_DEFAULT_PARAMETERS);

  //
  // Post-processing: Unpack and map query params per spec
  // ?installmentPeriod=once
  if (
    scrubbedQueryParams.installmentPeriod.toLowerCase() ===
    QUERY_PARAMETERS_STRING_VALUES.onceStr
  ) {
    // Set data for form submit
    scrubbedQueryParams = mapInstallmentPeriodOncetoForm(scrubbedQueryParams);
    // Set UI level with payment period selected state
    level = DEFAULT_ONCE_DONATION_LEVEL_WITH_INSTALL_PERIOD;
  }
  //
  // Set the Choices form state from defaults + query parameters
  //
  const { amount, payFees } = BUSINESS_BUCKETS[level];

  return {
    level,
    amount,
    pay_fees_value: payFees,
    campaign_id: scrubbedQueryParams.campaignId,
    referral_id: scrubbedQueryParams.referralId,
    installment_period: scrubbedQueryParams.installment_period,
    installments: scrubbedQueryParams.installments,
    openended_status: scrubbedQueryParams.openended_status,
  };
}

function createInitialFormState(queryParams) {
  if (window.__BUSINESS_FORM_REHYDRATION__) {
    return window.__BUSINESS_FORM_REHYDRATION__;
  }
  const dynamicState = getStateFromParams(queryParams);
  const staticState = {
    stripeEmail: '',
    business_name: '',
    website: '',
    shipping_street: '',
    shipping_city: '',
    shipping_state: DEFAULT_STATE_SELECTED,
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
    routes: [{ path: '/', component: RouteHandler }],
  });
}

function bindRouterEvents(router, routeHandler, store) {
  router.onReady(() => {
    const topForm = new Vue({ ...BusinessForm, store });

    const {
      currentRoute: { query },
    } = router;

    store.dispatch(
      'businessForm/createInitialState',
      createInitialFormState(query)
    );

    routeHandler.$mount('#app');
    topForm.$mount('#business-form');
    // wall.$mount('#business-wall');
  });
}

export { createRouter, bindRouterEvents };

// TEMPORARILY here == move to proper test
// Test strings
// http://local.texastribune.org/business?installments=None
//  http://local.texastribune.org/business?installmentPeriod=foo
//  http://local.texastribune.org/business?campaignId=ui903&installmentPeriod=once
//  http://local.texastribune.org/business?campaignId=ui903&installmentPeriod=once&foo=bar
//  http://local.texastribune.org/business?campaignId=ui903&installmentPeriod=once&<script>jk//∫ß
//  http://local.texastribune.org/business?campaignId=ui903&referralId=7ujhjhjhjheiwfioefu880348390483048328fdklvgjkvbhdfjkvhdsjhvbfjkgt439t748937t892347327t934797jhj&installmentPeriod=once&<script>jk//∫ß
// EMAILS
// fjpbarb+1@gmail.com
// Confuses validate js
// // ff+/;FLF@g.co
