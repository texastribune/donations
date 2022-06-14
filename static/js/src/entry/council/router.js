/* eslint-disable no-underscore-dangle, no-param-reassign */

import Vue from 'vue';
import VueRouter from 'vue-router';

import RouteHandler from '../../RouteHandler.vue';
import CouncilWall from './CouncilWall.vue';

Vue.use(VueRouter);

function createRouter() {
  return new VueRouter({
    base: '/council',
    mode: 'history',
    routes: [{ path: '/', component: RouteHandler }],
  });
}

function bindRouterEvents(router, routeHandler) {
  router.onReady(() => {
    const wall = new Vue({ ...CouncilWall });

    routeHandler.$mount('#app');
    wall.$mount('#council-wall');
  });
}

export { createRouter, bindRouterEvents };
