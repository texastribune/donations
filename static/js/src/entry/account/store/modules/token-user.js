/* eslint-disable no-param-reassign, camelcase */

import jwt from 'jsonwebtoken';
import { setExtra } from '@sentry/browser';

import auth from '../../utils/auth';
import { setFlag, clearFlag, isLoggedIn } from '../../utils/auth-actions';
import { LoggedOutError, Auth0Error } from '../../errors';

function createDefaultState() {
  return {
    accessToken: '',
    expiryInSeconds: 0,
    canViewAs: false,
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

  SET_DETAILS(state, details) {
    state.details = details;
  },
};

const actions = {
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
            commit('SET_DETAILS', authResult.idTokenPayload);
            commit('SET_EXPIRY_IN_SECONDS', authResult.expiresIn);
            setExtra('auth', authResult);
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
