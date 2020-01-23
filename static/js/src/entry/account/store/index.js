import Vue from 'vue';
import Vuex from 'vuex';

import userModule from './user';
import tokenUserModule from './token-user';
import contextModule from './context';
import { MODULES } from './types';

Vue.use(Vuex);

const store = new Vuex.Store({
  modules: {
    [MODULES.user]: userModule,
    [MODULES.tokenUser]: tokenUserModule,
    [MODULES.context]: contextModule,
  },
});

export default store;
