/* eslint-disable no-param-reassign */

import axios from 'axios';

import addFields from './utils/add-fields';
import getTokenIdentityId from './utils/get-token-identity-id';
import { PORTAL_API_URL } from '../../constants';

const MUTATION_TYPES = {
  setDetails: 'SET_DETAILS',
};

const mutations = {
  [MUTATION_TYPES.setDetails](state, details) {
    state.details = details;
  },
};

function createDefaultState() {
  return { details: {} };
}

const actions = {
  getOtherUser: async ({ commit, rootState }, email) => {
    const { accessToken } = rootState.tokenUser;
    const { data } = await axios.get(`${PORTAL_API_URL}persons/`, {
      params: { email },
      headers: { Authorization: `Bearer ${accessToken}` },
    });

    commit(MUTATION_TYPES.setDetails, addFields(data[0]));
  },

  getUser: async ({ commit, rootState }) => {
    const { accessToken } = rootState.tokenUser;
    const { data } = await axios.get(`${PORTAL_API_URL}self/`, {
      headers: { Authorization: `Bearer ${accessToken}` },
    });

    commit(MUTATION_TYPES.setDetails, addFields(data));
  },

  updateUser: async ({ dispatch, state, rootState }, updates) => {
    const { accessToken } = rootState.tokenUser;
    const { id: personId } = state.details;

    await axios.patch(
      `${PORTAL_API_URL}persons/${personId}`,
      { ...updates },
      {
        headers: { Authorization: `Bearer ${accessToken}` },
      }
    );

    await dispatch('getUser');
  },

  updateIdentity: async ({ dispatch, state, rootState }, updates) => {
    const {
      accessToken,
      details: { email: tokenEmail },
    } = rootState.tokenUser;
    const { id: personId, identities } = state.details;
    const identityId = getTokenIdentityId(identities, tokenEmail);

    await axios.patch(
      `${PORTAL_API_URL}persons/${personId}/identities/${identityId}`,
      { ...updates },
      {
        headers: { Authorization: `Bearer ${accessToken}` },
      }
    );

    await dispatch('getUser');
  },

  linkIdentity: async ({ state, rootState }, identity) => {
    const {
      accessToken,
      details: { email: tokenEmail },
    } = rootState.tokenUser;
    const { id: personId } = state.details;

    await axios.put(
      `${PORTAL_API_URL}persons/${personId}/identities/${tokenEmail}`,
      identity,
      {
        headers: { Authorization: `Bearer ${accessToken}` },
      }
    );
  },
};

export default {
  namespaced: true,
  state: createDefaultState(),
  mutations,
  actions,
  getters: {},
};
