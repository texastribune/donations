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
    isVerified: false,
    error: null,
    details: {},
  };
}

const MUTATION_TYPES = {
  setAccessToken: 'SET_ACCESS_TOKEN',
  setIsVerified: 'SET_IS_VERIFIED',
  setCanViewAs: 'SET_CAN_VIEW_AS',
  setDetails: 'SET_DETAILS',
  setError: 'SET_ERROR',
};

const mutations = {
  [MUTATION_TYPES.setAccessToken](state, accessToken) {
    state.accessToken = accessToken;
  },

  [MUTATION_TYPES.setIsVerified](state, isVerified) {
    state.isVerified = isVerified;
  },

  [MUTATION_TYPES.setCanViewAs](state, canViewAs) {
    state.canViewAs = canViewAs;
  },

  [MUTATION_TYPES.setDetails](state, details) {
    state.details = details;
  },

  [MUTATION_TYPES.setError](state, err) {
    state.error = new Auth0Error(err);
  },
};

const actions = {
  getTokenUser: ({ commit }) =>
    new Promise(resolve => {
      if (hasLoggedInFlag()) {
        auth.checkSession(
          { responseType: 'token id_token' },
          (err, authResult) => {
            if (err) {
              const { error, error_description } = err;
              // TODO: show fly-in
              if (error && error !== 'login_required') {
                // instead of throwing this up now so user gets
                // the error page, store it and only throw it when
                // user enters a login-required route; that logic is
                // handled in our route mixin
                commit(MUTATION_TYPES.setError, error_description);
              } else if (!error) {
                // from Auth0 docs: you can also get a generic 403 error
                // without an error or error_description property.
                commit(MUTATION_TYPES.setError, 'Auth0 unknown 403 error');
              }
              commit(MUTATION_TYPES.setAccessToken, '');
              clearFlag();
              resolve();
            } else {
              const { email_verified } = authResult.idTokenPayload;
              const { permissions } = jwt.decode(authResult.accessToken);
              const filteredPerms = permissions.filter(
                perm => perm === 'portal:view_as'
              );

              commit(MUTATION_TYPES.setIsVerified, email_verified);
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
