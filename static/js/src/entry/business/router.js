import Vue from 'vue';
import VueRouter from 'vue-router';

import RouteHandler from '../../RouteHandler.vue';
import BusinessForm from './BusinessForm.vue';
import Wall from './Wall.vue';
import {BUSINESS_BUCKETS, DEFAULT_PAY_FEES} from './constants';

Vue.use(VueRouter);

function getStateFromParams(queryParams) {
  const defaultLevel = 'levelAYearly';
  const { campaignId = '' } = queryParams;
  let { level = defaultLevel } = queryParams;

  if (!BUSINESS_BUCKETS[level]) level = defaultLevel;

  const {
    amount,
    installments,
    installmentPeriod,
    payFees,
  } = BUSINESS_BUCKETS[level];

  return {
    level,
    amount,
    installments,
    pay_fees_value: payFees,
    installment_period: installmentPeriod,
    campaign_id: campaignId,
  };
}

function createBaseFormState(queryParams) {
  const dynamicState = getStateFromParams(queryParams);
  const staticState = {
    stripeEmail: '',
    customerId: '',
    first_name: '',
    last_name: '',
    description: 'The Texas Tribune Business Membership',
    reason: '',
    zipcode: '',
    pay_fees_value: 'False',
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
    const wall = new Vue({ ...Wall });
    const { currentRoute: { query } } = router;

    store.dispatch(
      'businessForm/createInitialState',
      createBaseFormState(query),
    );

    routeHandler.$mount('#app');
    topForm.$mount('#business-form');
    wall.$mount('#business-wall');
  });
}

export { createRouter, bindRouterEvents };
