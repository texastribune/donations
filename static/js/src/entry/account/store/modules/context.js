/* eslint-disable no-param-reassign */

function createDefaultState() {
  return {
    isViewingAs: false,
    appIsFetching: false,
  };
}

const MUTATION_TYPES = {
  setIsViewingAs: 'SET_IS_VIEWING_AS',
  setAppIsFetching: 'SET_APP_IS_FETCHING',
};

const mutations = {
  [MUTATION_TYPES.setIsViewingAs](state, isViewingAs) {
    state.isViewingAs = isViewingAs;
  },

  [MUTATION_TYPES.setAppIsFetching](state, appIsFetching) {
    state.appIsFetching = appIsFetching;
  },
};

const actions = {
  setIsViewingAs: ({ commit }, isViewingAs) => {
    commit(MUTATION_TYPES.setIsViewingAs, isViewingAs);
  },

  setAppIsFetching: ({ commit }, appIsFetching) => {
    commit(MUTATION_TYPES.setAppIsFetching, appIsFetching);
  },
};

export default {
  namespaced: true,
  state: createDefaultState(),
  mutations,
  actions,
  getters: {},
};
