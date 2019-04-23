/* eslint-disable no-param-reassign */

function createDefaultState() {
  return {
    hasError: false,
  };
}

const mutations = {
  SET_ERROR(state, hasError) {
    state.hasError = hasError;
  },
};

const actions = {
  setError: ({ commit }, hasError) => {
    commit('SET_ERROR', hasError);
  },
};

export default {
  namespaced: true,
  state: createDefaultState(),
  mutations,
  actions,
  getters: {},
};
