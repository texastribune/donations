/* eslint-disable no-param-reassign */

function createDefaultState() {
  return {
    hasError: false,
    isFetching: false,
  };
}

const mutations = {
  SET_ERROR(state, hasError) {
    state.hasError = hasError;
  },

  SET_IS_FETCHING(state, isFetching) {
    state.isFetching = isFetching;
  },
};

const actions = {
  setError: ({ commit }, hasError) => {
    commit('SET_ERROR', hasError);
  },

  setIsFetching: ({ commit }, isFetching) => {
    commit('SET_IS_FETCHING', isFetching);
  },
};

export default {
  namespaced: true,
  state: createDefaultState(),
  mutations,
  actions,
  getters: {},
};
