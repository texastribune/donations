import Vue from 'vue';
import Vuex from 'vuex';

import userModule from './user';
import tokenUserModule from './token-user';
import contextModule from './context';
import { USER_MODULE, TOKEN_USER_MODULE, CONTEXT_MODULE } from '../constants';

Vue.use(Vuex);

const store = new Vuex.Store({
  modules: {
    [USER_MODULE]: userModule,
    [TOKEN_USER_MODULE]: tokenUserModule,
    [CONTEXT_MODULE]: contextModule,
  },
});

export default store;
