import Vue from 'vue';
import VueRouter from 'vue-router';

import RouteHandler from '../../RouteHandler.vue';
import CircleForm from './CircleForm.vue';
import Wall from './Wall.vue';
import { CIRCLE_BUCKETS } from './constants';

Vue.use(VueRouter);

function getStateFromParams(queryParams) {
  const defaultLevel = 'editorMonthly';
  const { campaignId = '', referralId = '' } = queryParams;
  let { level = defaultLevel } = queryParams;

  if (!CIRCLE_BUCKETS[level]) level = defaultLevel;

  const {
    amount,
    installments,
    installmentPeriod,
  } = CIRCLE_BUCKETS[level];

  return {
    level,
    amount,
    installments,
    installment_period: installmentPeriod,
    campaign_id: campaignId,
    referral_id: referralId,
  };
}

function createBaseFormState(queryParams) {
  const dynamicState = getStateFromParams(queryParams);
  const staticState = {
    stripeEmail: '',
    stripeToken: '',
    first_name: '',
    last_name: '',
    description: 'The Texas Tribune Circle Membership',
    reason: '',
    zipcode: '',
    pay_fees_value: 'False',
    openended_status: 'None',
  };

  return { ...staticState, ...dynamicState };
}

function createRouter() {
  return new VueRouter({
    base: '/circleform',
    mode: 'history',
    routes: [
      { path: '/', component: RouteHandler },
    ],
  });
}

function bindRouterEvents(router, routeHandler, store) {
  router.onReady(() => {
    const topForm = new Vue({ ...CircleForm, store });
    const wall = new Vue({ ...Wall });
    const { currentRoute: { query } } = router;

    store.dispatch(
      'circleForm/createInitialState',
      createBaseFormState(query),
    );

    routeHandler.$mount('#app');
    topForm.$mount('#circle-form');
    wall.$mount('#circle-wall');
  });
}

export { createRouter, bindRouterEvents };
