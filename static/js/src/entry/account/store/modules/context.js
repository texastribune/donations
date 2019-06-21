/* eslint-disable no-param-reassign */

function createDefaultState() {
  return {
    hasError: false,
    isUnverified: false,
    isViewingAs: false,
  };
}

const mutations = {
  SET_ERROR(state, hasError) {
    state.hasError = hasError;
  },

  SET_UNVERIFIED(state, isUnverified) {
    state.isUnverified = isUnverified;
  },

  SET_IS_VIEWING_AS(state, isViewingAs) {
    state.isViewingAs = isViewingAs;
  },
};

const actions = {
  setError: ({ commit }, hasError) => {
    commit('SET_ERROR', hasError);
  },

  setUnverified: ({ commit }, isUnverified) => {
    commit('SET_UNVERIFIED', isUnverified);
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
