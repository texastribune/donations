/* eslint-disable no-param-reassign */

import axios from 'axios';
// import camelCase from 'camelcase';

import { USER_TYPES } from '../types';
import getTokenIdentity from '../../utils/get-token-identity';
import { PORTAL_API_URL } from '../../constants';

const SET_RAW_DATA = 'SET_RAW_DATA';

const state = { data: {} };

const mutations = {
  [SET_RAW_DATA](currentState, data) {
    currentState.data = data;
  },
};

const actions = {
  [USER_TYPES.getOtherUser]: async ({ commit, rootState }, email) => {
    const { accessToken } = rootState.tokenUser;
    const { data } = await axios.get(`${PORTAL_API_URL}persons/`, {
      params: { email },
      headers: { Authorization: `Bearer ${accessToken}` },
    });

    commit(SET_RAW_DATA, data[0]);
  },

  [USER_TYPES.getUser]: async ({ commit, rootState }) => {
    const { accessToken } = rootState.tokenUser;
    const { data } = await axios.get(`${PORTAL_API_URL}self/`, {
      headers: { Authorization: `Bearer ${accessToken}` },
    });

    commit(SET_RAW_DATA, data);
  },

  [USER_TYPES.updateUser]: async (
    { state: moduleState, rootState },
    updates
  ) => {
    const { accessToken } = rootState.tokenUser;
    const { id: personId } = moduleState.data;

    await axios.patch(`${PORTAL_API_URL}persons/${personId}/`, updates, {
      headers: { Authorization: `Bearer ${accessToken}` },
    });
  },

  [USER_TYPES.updateIdentity]: async (
    { state: moduleState, rootState },
    updates
  ) => {
    const {
      accessToken,
      details: { email: tokenEmail },
    } = rootState.tokenUser;
    const { id: personId, identities } = moduleState.data;
    const { id: identityId } = getTokenIdentity(identities, tokenEmail);

    await axios.patch(
      `${PORTAL_API_URL}persons/${personId}/identities/${identityId}/`,
      updates,
      {
        headers: { Authorization: `Bearer ${accessToken}` },
      }
    );
  },

  [USER_TYPES.linkIdentity]: async (
    { state: moduleState, rootState },
    identity
  ) => {
    const {
      accessToken,
      details: { email: tokenEmail },
    } = rootState.tokenUser;
    const { id: personId } = moduleState.data;

    await axios.put(
      `${PORTAL_API_URL}persons/${personId}/identities/${tokenEmail}/`,
      identity,
      {
        headers: { Authorization: `Bearer ${accessToken}` },
      }
    );
  },

  [USER_TYPES.confirmLinkedIdentity]: async (
    { state: moduleState, rootState },
    ticket
  ) => {
    const {
      accessToken,
      details: { email: tokenEmail },
    } = rootState.tokenUser;
    const { id: personId } = moduleState.data;

    await axios.put(
      `${PORTAL_API_URL}persons/${personId}/identities/${tokenEmail}/?ticket=${ticket}`,
      {},
      {
        headers: { Authorization: `Bearer ${accessToken}` },
      }
    );
  },
};

const getters = {
  userId: () => {},
  tokenIdentity: () => {},
  isNeverGiven: () => {},
  isSingleDonor: () => {},
  isRecurringDonor: () => {},
  isCircleDonor: () => {},
  isCustomDonor: () => {},
  isExpired: () => {},
  isBlastSubscriber: () => {},
  hasGivenNotCustom: () => {},
  willExpire: () => {},
  membershipLevel: () => {},
};

export default {
  namespaced: true,
  state,
  mutations,
  actions,
  getters,
};
