import Vue from 'vue';
import VueRouter from 'vue-router';

import RouteHandler from '../../components/RouteHandler.vue';
import TopForm from '../../containers/TopForm.vue';

Vue.use(VueRouter);

function baseFormQueryChanges(queryParams) {
  let openEndedStatus;
  let { amount, installmentPeriod = 'monthly' } = queryParams;
  const { campaignId = '' } = queryParams;

  switch (installmentPeriod.toLowerCase()) {
    case 'monthly':
      openEndedStatus = 'Open';
      amount = amount || '10';
      break;
    case 'yearly':
      openEndedStatus = 'Open';
      amount = amount || '75';
      break;
    case 'once':
      openEndedStatus = 'None';
      installmentPeriod = 'None';
      amount = amount || '75';
      break;
    default:
      installmentPeriod = 'monthly';
      openEndedStatus = 'Open';
      amount = amount || '10';
  }

  return {
    amount,
    campaignId,
    installmentPeriod,
    openEndedStatus,
  };
}

function createRouter() {
  return new VueRouter({
    base: '/devdonate',
    mode: 'history',
    routes: [
      { path: '/', component: RouteHandler },
    ],
  });
}

function bindRouterEvents(router, routeHandler, store) {
  router.onReady(() => {
    const topForm = new Vue({ ...TopForm, store });
    const { currentRoute: { query } } = router;

    store.dispatch(
      'baseForm/createInitialState',
      {
        ...{ foo: 'bar' },
        ...baseFormQueryChanges(query),
      },
    );

    routeHandler.$mount('#app');
    topForm.$mount('#top-form');

    router.beforeEach((to, from, next) => {
      store.dispatch(
        'baseForm/updateValues',
        baseFormQueryChanges(to.query),
      );
      next();
    });
  });
}

export { createRouter, bindRouterEvents };
