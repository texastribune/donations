/* eslint-disable no-param-reassign */

import { CONTEXT_TYPES } from '../types';

const SET_IS_FETCHING = 'SET_IS_FETCHING';
const SET_ERROR = 'SET_ERROR';

const initialState = {
  isFetching: false,
  error: null,
};

const mutations = {
  [SET_IS_FETCHING](state, isFetching) {
    state.isFetching = isFetching;
  },

  [SET_ERROR](state, error) {
    state.error = error;
  },
};

const actions = {
  [CONTEXT_TYPES.setIsFetching]: ({ commit }, isFetching) => {
    commit(SET_IS_FETCHING, isFetching);
  },

  [CONTEXT_TYPES.setError]: ({ commit }, error) => {
    commit(SET_ERROR, error);
  },
};

const getters = {
  isViewingAs: (_, __, { user: { viewAsEmail } }) => !!viewAsEmail,
};

export default {
  namespaced: true,
  state: initialState,
  mutations,
  actions,
  getters,
};
