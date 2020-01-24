import Vue from 'vue';
import Vuex from 'vuex';

import userModule from './user';
import tokenUserModule from './token-user';
import contextModule from './context';

Vue.use(Vuex);

const store = new Vuex.Store({
  modules: {
    user: userModule,
    tokenUser: tokenUserModule,
    context: contextModule,
  },
});

export default store;
