/* eslint-disable no-param-reassign */

import logError from '../../utils/log-error';

function createDefaultState() {
  return {
    error: null,
    isUnverified: false,
    isViewingAs: false,
    appIsFetching: false,
  };
}

const MUTATION_TYPES = {
  setError: 'SET_ERROR',
  setUnverified: 'SET_UNVERIFIED',
  setIsViewingAs: 'SET_IS_VIEWING_AS',
  setAppIsFetching: 'SET_APP_IS_FETCHING',
};

const mutations = {
  [MUTATION_TYPES.setError](state, err) {
    state.error = err;
  },

  [MUTATION_TYPES.setUnverified](state) {
    state.isUnverified = true;
  },

  [MUTATION_TYPES.setIsViewingAs](state, isViewingAs) {
    state.isViewingAs = isViewingAs;
  },

  [MUTATION_TYPES.setAppIsFetching](state, appIsFetching) {
    state.appIsFetching = appIsFetching;
  },
};

const actions = {
  setError: ({ commit }, err) => {
    logError(err);
    commit(MUTATION_TYPES.setError, err);
  },

  setUnverified: ({ commit }) => {
    commit(MUTATION_TYPES.setUnverified);
  },

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
