/* eslint-disable no-param-reassign */

const MUTATION_TYPES = {
  setIsViewingAs: 'SET_IS_VIEWING_AS',
  setIsFetching: 'SET_IS_FETCHING',
  setError: 'SET_ERROR',
};

function createDefaultState() {
  return {
    isViewingAs: false,
    isFetching: false,
    error: null,
  };
}

const mutations = {
  [MUTATION_TYPES.setIsViewingAs](state, isViewingAs) {
    state.isViewingAs = isViewingAs;
  },

  [MUTATION_TYPES.setIsFetching](state, isFetching) {
    state.isFetching = isFetching;
  },

  [MUTATION_TYPES.setError](state, error) {
    state.error = error;
  },
};

const actions = {
  setIsViewingAs: ({ commit }, isViewingAs) => {
    commit(MUTATION_TYPES.setIsViewingAs, isViewingAs);
  },

  setIsFetching: ({ commit }, isFetching) => {
    commit(MUTATION_TYPES.setIsFetching, isFetching);
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
