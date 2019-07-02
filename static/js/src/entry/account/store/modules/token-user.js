/* eslint-disable no-param-reassign, camelcase */

import jwt from 'jsonwebtoken';
import { setExtra } from '@sentry/browser';

import auth from '../../utils/auth';
import { setFlag, clearFlag, hasLoggedInFlag } from '../../utils/auth-actions';
import { Auth0Error } from '../../errors';

function createDefaultState() {
  return {
    accessToken: '',
    canViewAs: false,
    error: null,
    details: {},
  };
}

const MUTATION_TYPES = {
  setAccessToken: 'SET_ACCESS_TOKEN',
  setCanViewAs: 'SET_CAN_VIEW_AS',
  setDetails: 'SET_DETAILS',
  setError: 'SET_ERROR',
};

const mutations = {
  [MUTATION_TYPES.setAccessToken](state, accessToken) {
    state.accessToken = accessToken;
  },

  [MUTATION_TYPES.setCanViewAs](state, canViewAs) {
    state.canViewAs = canViewAs;
  },

  [MUTATION_TYPES.setDetails](state, details) {
    state.details = details;
  },

  [MUTATION_TYPES.setError](state, error) {
    state.error = new Auth0Error(error.error);
  },
};

const actions = {
  getTokenUser: ({ commit }) =>
    new Promise(resolve => {
      if (hasLoggedInFlag()) {
        auth.checkSession(
          { responseType: 'token id_token' },
          (err, authResult) => {
            if (err && err.error === 'login_required') {
              // reset because of refresh polling
              commit(MUTATION_TYPES.setAccessToken, '');
              clearFlag();
              resolve();
            } else if (err) {
              commit(MUTATION_TYPES.setError, err);
              clearFlag();
              resolve();
            } else {
              const { permissions } = jwt.decode(authResult.accessToken);
              const filteredPerms = permissions.filter(
                perm => perm === 'portal:view_as'
              );

              commit(MUTATION_TYPES.setCanViewAs, filteredPerms.length === 1);
              commit(MUTATION_TYPES.setAccessToken, authResult.accessToken);
              commit(MUTATION_TYPES.setDetails, authResult.idTokenPayload);
              setExtra('auth', authResult.idTokenPayload);
              setFlag();
              resolve();
            }
          }
        );
      } else {
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
