/* eslint-disable no-param-reassign */

import axios from 'axios';
import jwt from 'jsonwebtoken';

import auth from '../../utils/auth';
import { setFlag, clearFlag, isLoggedIn } from '../../utils/auth-actions';
import {
  LoggedOutError,
  Auth0Error,
  MultiplePersonsError,
  NoPersonsError,
} from '../../errors';
import { PORTAL_API_URL } from '../../constants';

// import response from '../../dummy/recurring.json';
// import response from '../../dummy/one_time_canceled_blast.json';
// import response from '../../dummy/never_given.json';
// import response from '../../dummy/recurring_expired_and_blast.json';

function createDefaultState() {
  return {
    accessToken: '',
    expiryInSeconds: 0,
    canViewAs: false,
    tokenDetails: {},
    details: {},
  };
}

const mutations = {
  SET_ACCESS_TOKEN(state, accessToken) {
    state.accessToken = accessToken;
  },

  SET_EXPIRY_IN_SECONDS(state, expiryInSeconds) {
    state.expiryInSeconds = expiryInSeconds;
  },

  SET_CAN_VIEW_AS(state, canViewAs) {
    state.canViewAs = canViewAs;
  },

  SET_TOKEN_DETAILS(state, tokenDetails) {
    state.tokenDetails = tokenDetails;
  },

  SET_DETAILS(state, details) {
    state.details = details;
  },
};

const actions = {
  getOtherUser: async ({ commit, state }, email) => {
    const { data } = await axios.get(`${PORTAL_API_URL}persons/`, {
      params: { email },
      headers: { Authorization: `Bearer ${state.accessToken}` },
    });

    if (!data.length) throw new NoPersonsError();
    if (data.length > 1) throw new MultiplePersonsError();

    commit('SET_DETAILS', data[0]);
  },

  getUser: async ({ commit, state }) => {
    const { data } = await axios.get(`${PORTAL_API_URL}self/`, {
      headers: { Authorization: `Bearer ${state.accessToken}` },
    });

    commit('SET_DETAILS', data);
  },

  getTokenUser: ({ commit }) =>
    new Promise((resolve, reject) => {
      if (isLoggedIn()) {
        auth.checkSession(
          { responseType: 'token id_token' },
          (err, authResult) => {
            if (err && err.error === 'login_required') {
              commit('SET_ACCESS_TOKEN', '');
              clearFlag();
              return reject(new LoggedOutError());
            }

            if (
              err ||
              !authResult ||
              !authResult.accessToken ||
              !authResult.idTokenPayload ||
              !authResult.expiresIn
            ) {
              clearFlag();
              return reject(new Auth0Error());
            }

            const { permissions } = jwt.decode(authResult.accessToken);
            const filteredPerms = permissions.filter(
              perm => perm === 'portal:view_as'
            );

            commit('SET_CAN_VIEW_AS', filteredPerms.length === 1);
            commit('SET_ACCESS_TOKEN', authResult.accessToken);
            commit('SET_TOKEN_DETAILS', authResult.idTokenPayload);
            commit('SET_EXPIRY_IN_SECONDS', authResult.expiresIn);
            setFlag();
            return resolve();
          }
        );
      } else {
        clearFlag();
        reject(new LoggedOutError());
      }
    }),
};

export default {
  namespaced: true,
  state: createDefaultState(),
  mutations,
  actions,
  getters: {},
};
