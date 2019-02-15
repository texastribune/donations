/* eslint-disable no-underscore-dangle, no-param-reassign */

import Vue from 'vue';
import VueRouter from 'vue-router';

import RouteHandler from '../../RouteHandler.vue';
import TopForm from './TopForm.vue';
import queryParamScrub from '../../utils/queryParamScrub';
import mergeValuesIntoStartState from '../../utils/mergeValuesIntoStartState';

import {
  BUSINESS_BUCKETS,
  BUSINESS_FORM_STATE,
  DEFAULT_DONATION_LEVEL_WITH_INSTALL_PERIOD,
  DEFAULT_ONCE_DONATION_LEVEL_WITH_INSTALL_PERIOD,
  WL_DEFAULT_PARAMETERS,
  WL_QUERY_PARAMETERS_MAX_NBR_CHARS,
  WL_QUERY_ESCAPE_THRESHOLD,
  QUERY_PARAMETERS_STRING_VALUES,
} from './constants';

Vue.use(VueRouter);

function mapInstallmentPeriodOncetoForm(finalSanitizedParams) {
  // set data for form submit
  finalSanitizedParams.installments = QUERY_PARAMETERS_STRING_VALUES.oneStr;
  finalSanitizedParams.installment_period =
    QUERY_PARAMETERS_STRING_VALUES.noneStr;
  finalSanitizedParams.openended_status =
    QUERY_PARAMETERS_STRING_VALUES.noneStr;

  return finalSanitizedParams;
}

function getStateFromParams(queryParams) {
  let level = DEFAULT_DONATION_LEVEL_WITH_INSTALL_PERIOD;
  let scrubbedQueryParams;

  // if this query is within the threshold number of parameters
  // filter input query oarams using the app whitelist
  if (Object.keys(queryParams).length <= WL_QUERY_ESCAPE_THRESHOLD) {
    scrubbedQueryParams = queryParamScrub(
      queryParams,
      WL_DEFAULT_PARAMETERS,
      WL_QUERY_PARAMETERS_MAX_NBR_CHARS
    );
  } else {
    scrubbedQueryParams = WL_DEFAULT_PARAMETERS;
  }

  if (
    scrubbedQueryParams.installmentPeriod.toLowerCase() ===
    QUERY_PARAMETERS_STRING_VALUES.onceStr
  ) {
    // set data for form submit
    scrubbedQueryParams = mapInstallmentPeriodOncetoForm(scrubbedQueryParams);
    // set UI level with payment period selected state
    level = DEFAULT_ONCE_DONATION_LEVEL_WITH_INSTALL_PERIOD;
  }

  // set the choices form state from defaults + query parameters
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

    const {
      currentRoute: { query },
    } = router;

    store.dispatch(
      'businessForm/createInitialState',
      createInitialFormState(query)
    );

    routeHandler.$mount('#app');
    topForm.$mount('#business-form');
  });
}

export { createRouter, bindRouterEvents };
