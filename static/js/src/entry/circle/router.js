import Vue from 'vue';
import VueRouter from 'vue-router';

import RouteHandler from '../../RouteHandler.vue';
import CircleForm from './CircleForm.vue';

Vue.use(VueRouter);

function createBaseFormState(queryParams) {
  const baseState = {
    stripeEmail: '',
    customerId: '',
    first_name: '',
    last_name: '',
    description: 'The Texas Tribune Membership',
    reason: '',
    zipcode: '',
    pay_fees_value: 'False',
    openended_status: 'None',
  };

  let installments;
  let { amount, installmentPeriod = 'monthly' } = queryParams;
  const { campaignId = '' } = queryParams;

  switch (installmentPeriod.toLowerCase()) {
    case 'monthly':
      amount = amount || '84';
      installments = '36';
      break;
    case 'yearly':
      amount = amount || '1000';
      installments = '3';
      break;
    default:
      installmentPeriod = 'monthly';
      amount = amount || '84';
      installments = '36';
  }

  return {
    ...baseState,
    amount,
    installments,
    campaign_id: campaignId,
    installment_period: installmentPeriod,
  };
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
    const { currentRoute: { query } } = router;

    store.dispatch(
      'circleForm/createInitialState',
      createBaseFormState(query),
    );

    routeHandler.$mount('#app');
    topForm.$mount('#circle-form');
  });
}

export { createRouter, bindRouterEvents };
