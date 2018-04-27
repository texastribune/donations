import Vue from 'vue';

import App from '../../App.vue';
import { createRouter, bindRouterEvents } from './router';
import createStore from './createStore';

const store = createStore();
const router = createRouter();

const routeHandler = new Vue({ ...App, router });

bindRouterEvents(router, routeHandler, store);
