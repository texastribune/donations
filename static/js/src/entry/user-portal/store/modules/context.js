/* eslint-disable no-param-reassign */

function createDefaultState() {
  return {
    hasError: false,
    isUnverified: false,
  };
}

const mutations = {
  SET_ERROR(state, hasError) {
    state.hasError = hasError;
  },

  SET_UNVERIFIED(state, isUnverified) {
    state.isUnverified = isUnverified;
  },
};

const actions = {
  setError: ({ commit }, hasError) => {
    commit('SET_ERROR', hasError);
  },

  setUnverified: ({ commit }, isUnverified) => {
    commit('SET_UNVERIFIED', isUnverified);
  },
};

export default {
  namespaced: true,
  state: createDefaultState(),
  mutations,
  actions,
  getters: {},
};
