/* eslint-disable no-param-reassign, camelcase */

import jwt from 'jsonwebtoken';
import { setExtra } from '@sentry/browser';

import auth from '../../utils/auth';
import { setFlag, clearFlag, isLoggedIn } from '../../utils/auth-actions';
import { Auth0Error } from '../../errors';

function createDefaultState() {
  return {
    accessToken: '',
    expiryInSeconds: 0,
    canViewAs: false,
    details: {},
  };
}

const MUTATION_TYPES = {
  setAccessToken: 'SET_ACCESS_TOKEN',
  setExpiryInSeconds: 'SET_EXPIRY_IN_SECONDS',
  setCanViewAs: 'SET_CAN_VIEW_AS',
  setDetails: 'SET_DETAILS',
};

const mutations = {
  [MUTATION_TYPES.setAccessToken](state, accessToken) {
    state.accessToken = accessToken;
  },

  [MUTATION_TYPES.setExpiryInSeconds](state, expiryInSeconds) {
    state.expiryInSeconds = expiryInSeconds;
  },

  [MUTATION_TYPES.setCanViewAs](state, canViewAs) {
    state.canViewAs = canViewAs;
  },

  [MUTATION_TYPES.setDetails](state, details) {
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
              commit(MUTATION_TYPES.setAccessToken, '');
              clearFlag();
              resolve();
            } else if (
              err ||
              !authResult ||
              !authResult.accessToken ||
              !authResult.idTokenPayload ||
              !authResult.expiresIn
            ) {
              clearFlag();
              reject(new Auth0Error(err.error));
            } else {
              const { permissions } = jwt.decode(authResult.accessToken);
              const filteredPerms = permissions.filter(
                perm => perm === 'portal:view_as'
              );

              commit(MUTATION_TYPES.setCanViewAs, filteredPerms.length === 1);
              commit(MUTATION_TYPES.setAccessToken, authResult.accessToken);
              commit(MUTATION_TYPES.setDetails, authResult.idTokenPayload);
              commit(MUTATION_TYPES.setExpiryInSeconds, authResult.expiresIn);
              setExtra('auth', authResult.idTokenPayload);
              setFlag();
              resolve();
            }
          }
        );
      } else {
        clearFlag();
        resolve();
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
