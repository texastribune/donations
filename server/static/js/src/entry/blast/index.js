import Vue from 'vue';
import Vuex from 'vuex';

import App from '../../App.vue';
import connectedFormModule from '../../store/modules/connected-form';
import { createRouter, bindRouterEvents } from './router';
import cssClasses from '../../mixins/global/css-classes';
import gtm from '../../mixins/global/gtm';

Vue.use(Vuex);
Vue.mixin(cssClasses);
Vue.mixin(gtm);

const store = new Vuex.Store({
  modules: {
    blastForm: connectedFormModule,
  },
});
const router = createRouter();
const routeHandler = new Vue({ ...App, router });

bindRouterEvents(router, routeHandler, store);
