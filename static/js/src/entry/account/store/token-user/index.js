/* eslint-disable no-param-reassign */

import jwt from 'jsonwebtoken';
import { setExtra } from '@sentry/browser';

import { TOKEN_USER_TYPES } from '../types';
import auth from '../../utils/auth';
import { Auth0Error } from '../../errors';

const SET_READY = 'SET_READY';
const SET_LOGGED_OUT = 'SET_LOGGED_OUT';
const SET_ERROR = 'SET_ERROR';

const initialState = {
  isLoggedIn: false,
  accessToken: '',
  accessTokenPayload: {},
  idToken: '',
  idTokenPayload: {},
  error: null,
};

const mutations = {
  [SET_READY](state, { accessToken, idToken }) {
    const accessTokenPayload = jwt.decode(accessToken);
    const idTokenPayload = jwt.decode(idToken);

    state.isLoggedIn = true;
    state.accessToken = accessToken;
    state.accessTokenPayload = accessTokenPayload;
    state.idToken = idToken;
    state.idTokenPayload = idTokenPayload;
    state.error = null;

    setExtra('auth', idTokenPayload);
  },

  [SET_LOGGED_OUT](state) {
    state.isLoggedIn = false;
    state.accessToken = '';
    state.accessTokenPayload = {};
    state.idToken = '';
    state.idTokenPayload = {};
    state.error = null;

    setExtra('auth', {});
  },

  [SET_ERROR](state, error) {
    state.isLoggedIn = true;
    state.accessToken = '';
    state.accessTokenPayload = {};
    state.idToken = '';
    state.idTokenPayload = {};
    state.error = error;

    setExtra('auth', {});
  },
};

const actions = {
  [TOKEN_USER_TYPES.getTokenUser]: async ({ commit }) => {
    try {
      await new Promise((resolve, reject) => {
        auth.checkSession(
          { responseType: 'token id_token' },
          (err, authResult) => {
            if (err) {
              reject(err);
            } else {
              commit(SET_READY, {
                accessToken: authResult.accessToken,
                idToken: authResult.idToken,
              });
              resolve();
            }
          }
        );
      });
    } catch (err) {
      const { code, description } = err;

      if (code === 'login_required') {
        commit(SET_LOGGED_OUT);
      } else if (!code || !description) {
        commit(
          SET_ERROR,
          new Auth0Error({ message: 'Unknown error', code: 403 })
        );
      } else {
        commit(SET_ERROR, new Auth0Error({ message: description, code }));
      }
    }
  },
};

const getters = {
  tokenExpiryInMs: ({ accessTokenPayload: { exp = 0 } }) => exp * 1000,

  isReady: ({ isLoggedIn, error }) => isLoggedIn && !error,

  canViewAs: ({ accessTokenPayload }) => {
    const { permissions = [] } = accessTokenPayload;
    const filteredPerms = permissions.filter(perm => perm === 'portal:view_as');

    return filteredPerms.length === 1;
  },

  isVerified: ({ idTokenPayload: { email_verified: isVerified = false } }) =>
    isVerified,
};

export default {
  namespaced: true,
  state: initialState,
  mutations,
  actions,
  getters,
};
