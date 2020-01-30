/* eslint-disable no-param-reassign */

import jwt from 'jsonwebtoken';
import { setExtra } from '@sentry/browser';

import { TOKEN_USER_TYPES } from '../types';
import auth from '../../utils/auth';
import { clearLoggedInFlag, getLoggedInFlag } from '../../utils/storage';
import { Auth0Error } from '../../errors';

const SET_ACCESS_TOKEN = 'SET_ACCESS_TOKEN';
const SET_ID_TOKEN = 'SET_ID_TOKEN';
const SET_ID_TOKEN_PAYLOAD = 'SET_ID_TOKEN_PAYLOAD';
const SET_ERROR = 'SET_ERROR';

const initialState = {
  accessToken: '',
  accessTokenPayload: {},
  idToken: '',
  idTokenPayload: {},
  error: null,
};

const mutations = {
  [SET_ACCESS_TOKEN](state, accessToken) {
    state.accessToken = accessToken;
    state.accessTokenPayload = jwt.decode(accessToken);
  },

  [SET_ID_TOKEN](state, idToken) {
    state.idToken = idToken;
  },

  [SET_ID_TOKEN_PAYLOAD](state, payload) {
    state.idTokenPayload = payload;
  },

  [SET_ERROR](state, error) {
    state.error = new Auth0Error(error);
  },
};

const actions = {
  [TOKEN_USER_TYPES.getTokenUser]: ({ commit }) =>
    new Promise(resolve => {
      if (getLoggedInFlag() === 'true') {
        auth.checkSession(
          { responseType: 'token id_token' },
          (err, authResult) => {
            if (err) {
              const { error, error_description: description } = err;
              // TODO: show fly-in
              if (error && error !== 'login_required') {
                // instead of throwing this up now so user gets
                // the error page, store it and only throw it when
                // user enters a login-required route; that logic is
                // handled in our route mixin
                commit(SET_ERROR, description);
              } else if (!error) {
                // from Auth0 docs: you can also get a generic 403 error
                // without an error or error_description property.
                commit(SET_ERROR, 'Auth0 unknown 403 error');
              }
              commit(SET_ACCESS_TOKEN, '');
              clearLoggedInFlag();
              resolve();
            } else {
              commit(SET_ACCESS_TOKEN, authResult.accessToken);
              commit(SET_ID_TOKEN_PAYLOAD, authResult.idTokenPayload);
              setExtra('auth', authResult.idTokenPayload);
              resolve();
            }
          }
        );
      } else {
        resolve();
      }
    }),
};

const getters = {
  isLoggedIn: ({ accessToken }) => !!accessToken,

  canViewAs: ({ accessTokenPayload }) => {
    const { permissions } = accessTokenPayload;
    const filteredPerms = permissions.filter(perm => perm === 'portal:view_as');

    return filteredPerms.length === 1;
  },

  isVerified: ({ idTokenPayload: { email_verified: isVerified } }) =>
    isVerified,
};

export default {
  namespaced: true,
  state: initialState,
  mutations,
  actions,
  getters,
};
