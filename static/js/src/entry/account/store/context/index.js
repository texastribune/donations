/* eslint-disable no-param-reassign */

const MUTATION_TYPES = {
  setIsViewingAs: 'SET_IS_VIEWING_AS',
  setAppIsFetching: 'SET_APP_IS_FETCHING',
  setError: 'SET_ERROR',
};

function createDefaultState() {
  return {
    isViewingAs: false,
    appIsFetching: false,
    error: null,
  };
}

const mutations = {
  [MUTATION_TYPES.setIsViewingAs](state, isViewingAs) {
    state.isViewingAs = isViewingAs;
  },

  [MUTATION_TYPES.setAppIsFetching](state, appIsFetching) {
    state.appIsFetching = appIsFetching;
  },

  [MUTATION_TYPES.setError](state, error) {
    state.error = error;
  },
};

const actions = {
  setIsViewingAs: ({ commit }, isViewingAs) => {
    commit(MUTATION_TYPES.setIsViewingAs, isViewingAs);
  },

  setAppIsFetching: ({ commit }, appIsFetching) => {
    commit(MUTATION_TYPES.setAppIsFetching, appIsFetching);
  },

  setError: ({ commit }, error) => {
    commit(MUTATION_TYPES.setError, error);
  },
};

export default {
  namespaced: true,
  state: createDefaultState(),
  mutations,
  actions,
  getters: {},
};
