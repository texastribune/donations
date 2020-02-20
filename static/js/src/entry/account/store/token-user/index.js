/* eslint-disable no-param-reassign */

import jwt from 'jsonwebtoken';
import { setExtra } from '@sentry/browser';

import { TOKEN_USER_TYPES } from '../types';
import auth from '../../utils/auth';
import { clearLoggedInFlag, getLoggedInFlag } from '../../utils/auth-actions';
import { Auth0Error } from '../../errors';

const SET_ACCESS_TOKEN = 'SET_ACCESS_TOKEN';
const SET_ID_TOKEN = 'SET_ID_TOKEN';
const SET_ERROR = 'SET_ERROR';
const CLEAR_TOKENS = 'CLEAR_TOKENS';

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
    const payload = jwt.decode(idToken);

    state.idToken = idToken;
    state.idTokenPayload = payload;

    setExtra('auth', payload);
  },

  [CLEAR_TOKENS](state) {
    state.idToken = '';
    state.idTokenPayload = {};
    state.accessToken = '';
    state.accessTokenPayload = {};

    setExtra('auth', {});
  },

  [SET_ERROR](state, { description, code }) {
    state.error = new Auth0Error({ message: description, code });
  },
};

const actions = {
  [TOKEN_USER_TYPES.getTokenUser]: async ({ commit }) => {
    try {
      await new Promise((resolve, reject) => {
        if (getLoggedInFlag()) {
          auth.checkSession(
            { responseType: 'token id_token' },
            (err, authResult) => {
              if (err) {
                reject(err);
              } else {
                commit(SET_ACCESS_TOKEN, authResult.accessToken);
                commit(SET_ID_TOKEN, authResult.idToken);
                resolve();
              }
            }
          );
        } else {
          resolve();
        }
      });
    } catch (err) {
      const { code, description } = err;

      if (code === 'login_required') {
        clearLoggedInFlag();
      } else if (!code || !description) {
        commit(SET_ERROR, { code: 403, description: 'Unknown error' });
      } else {
        commit(SET_ERROR, { code, description });
      }

      commit(CLEAR_TOKENS);
    }
  },
};

const getters = {
  isLoggedIn: ({ accessToken }) => !!accessToken,

  canViewAs: ({ accessTokenPayload }) => {
    const { permissions = [] } = accessTokenPayload;
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
