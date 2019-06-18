/* eslint-disable no-param-reassign */

import logError from '../../utils/log-error';

function createDefaultState() {
  return {
    error: null,
    isUnverified: false,
  };
}

const mutations = {
  SET_ERROR(state, err) {
    state.error = err;
  },

  SET_UNVERIFIED(state) {
    state.isUnverified = true;
  },
};

const actions = {
  setError: ({ commit }, err) => {
    logError(err);
    commit('SET_ERROR', err);
  },

  setUnverified: ({ commit }) => {
    commit('SET_UNVERIFIED');
  },
};

export default {
  namespaced: true,
  state: createDefaultState(),
  mutations,
  actions,
  getters: {},
};
