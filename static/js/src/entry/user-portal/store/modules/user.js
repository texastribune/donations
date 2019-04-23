/* eslint-disable no-param-reassign */

import axios from 'axios';

import auth from '../../utils/auth';
import {
  extractUser,
  setFlag,
  clearFlag,
  isLoggedIn,
} from '../../utils/auth-actions';
import { LoggedOutError, Auth0Error } from '../../errors';

function createDefaultState() {
  return {
    token: '',
    details: {
      nickname: '',
      email: '',
      emailVerified: false,
    },
  };
}

const mutations = {
  SET_TOKEN(state, token) {
    state.token = token;
  },

  SET_DETAILS(state, details) {
    state.details = details;
  },
};

const actions = {
  getUser: ({ commit }) =>
    new Promise((resolve, reject) => {
      if (isLoggedIn()) {
        auth.checkSession(
          { responseType: 'id_token token' },
          (err, authResult) => {
            const { idToken, accessToken, idTokenPayload } = authResult;

            if (err && err.error === 'login_required') {
              clearFlag();
              return reject(new LoggedOutError());
            }
            if (err || !idToken || !accessToken || !idTokenPayload) {
              clearFlag();
              return reject(new Auth0Error());
            }

            commit('SET_TOKEN', idToken);
            commit('SET_DETAILS', extractUser(idTokenPayload));
            axios.defaults.headers.common.Authorization = `Bearer ${accessToken}`;
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
