import Vue from 'vue';
import Vuex from 'vuex';

import userModule from './modules/user';
import contextModule from './modules/context';

Vue.use(Vuex);

const store = new Vuex.Store({
  modules: {
    user: userModule,
    context: contextModule,
  },
});

export default store;
