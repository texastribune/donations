import Vue from 'vue';
import Vuex from 'vuex';

import userModule from './modules/user';
import tokenUserModule from './modules/token-user';
import contextModule from './modules/context';

Vue.use(Vuex);

const store = new Vuex.Store({
  modules: {
    user: userModule,
    tokenUser: tokenUserModule,
    context: contextModule,
  },
});

export default store;
