/* eslint-disable no-param-reassign */

import axios from 'axios';

import addFields from './add-fields';
import { PORTAL_API_URL } from '../../constants';

const MUTATION_TYPES = {
  setDetails: 'SET_DETAILS',
  setIsFetching: 'SET_IS_FETCHING',
};

const mutations = {
  [MUTATION_TYPES.setDetails](state, details) {
    state.details = details;
  },

  [MUTATION_TYPES.setIsFetching](state, isFetching) {
    state.isFetching = isFetching;
  },
};

function createDefaultState() {
  return {
    details: {},
    isFetching: false,
  };
}

const actions = {
  getOtherUser: async ({ commit, rootState }, email) => {
    commit(MUTATION_TYPES.setIsFetching, true);

    const { accessToken } = rootState.tokenUser;
    const { data } = await axios.get(`${PORTAL_API_URL}persons/`, {
      params: { email },
      headers: { Authorization: `Bearer ${accessToken}` },
    });

    commit(MUTATION_TYPES.setDetails, addFields(data[0]));
    commit(MUTATION_TYPES.setIsFetching, false);
  },

  getUser: async ({ commit, rootState }) => {
    commit(MUTATION_TYPES.setIsFetching, true);

    const { accessToken } = rootState.tokenUser;
    const { data } = await axios.get(`${PORTAL_API_URL}self/`, {
      headers: { Authorization: `Bearer ${accessToken}` },
    });

    commit(MUTATION_TYPES.setDetails, addFields(data));
    commit(MUTATION_TYPES.setIsFetching, false);
  },
};

export default {
  namespaced: true,
  state: createDefaultState(),
  mutations,
  actions,
  getters: {},
};
