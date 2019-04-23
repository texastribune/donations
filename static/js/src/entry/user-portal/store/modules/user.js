/* eslint-disable no-param-reassign */

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
        auth.checkSession({ responseType: 'id_token' }, (err, authResult) => {
          const isValidResult = authResult && authResult.idToken;

          if (err && err.error === 'login_required') {
            clearFlag();
            return reject(new LoggedOutError());
          }
          if (err || !isValidResult) {
            clearFlag();
            return reject(new Auth0Error());
          }

          const user = extractUser(authResult.idTokenPayload);
          commit('SET_TOKEN', authResult.idToken);
          commit('SET_DETAILS', user);
          setFlag();
          return resolve(user);
        });
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
