/* eslint-disable no-param-reassign */

import logError from '../../utils/log-error';

function createDefaultState() {
  return {
    error: null,
    isUnverified: false,
    isViewingAs: false,
  };
}

const mutations = {
  SET_ERROR(state, err) {
    state.error = err;
  },

  SET_UNVERIFIED(state) {
    state.isUnverified = true;
  },

  SET_IS_VIEWING_AS(state, isViewingAs) {
    state.isViewingAs = isViewingAs;
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

  setIsViewingAs: ({ commit }, isViewingAs) => {
    commit('SET_IS_VIEWING_AS', isViewingAs);
  },
};

export default {
  namespaced: true,
  state: createDefaultState(),
  mutations,
  actions,
  getters: {},
};
