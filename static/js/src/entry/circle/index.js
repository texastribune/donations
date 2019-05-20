import Vue from 'vue';
import Vuex from 'vuex';

import App from '../../App.vue';
import FormModule from '../../store/modules/form';
import { createRouter, bindRouterEvents } from './router';
import cssClasses from '../../mixins/global/cssClasses';
import gtm from '../../mixins/global/gtm';

Vue.use(Vuex);
Vue.mixin(cssClasses);
Vue.mixin(gtm);

const store = new Vuex.Store({
  modules: {
    circleForm: FormModule,
  },
});
const router = createRouter();
const routeHandler = new Vue({ ...App, router });

bindRouterEvents(router, routeHandler, store);
