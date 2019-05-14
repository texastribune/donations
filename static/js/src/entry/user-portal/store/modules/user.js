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
    idToken: '',
    accessToken: '',
    details: {
      nickname: '',
      email: '',
      emailVerified: false,
    },
  };
}

const mutations = {
  SET_ID_TOKEN(state, idToken) {
    state.idToken = idToken;
  },

  SET_ACCESS_TOKEN(state, accessToken) {
    state.accessToken = accessToken;
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
            if (err && err.error === 'login_required') {
              clearFlag();
              return reject(new LoggedOutError());
            }
            if (
              err ||
              !authResult ||
              !authResult.idToken ||
              !authResult.accessToken ||
              !authResult.idTokenPayload
            ) {
              clearFlag();
              return reject(new Auth0Error());
            }

            commit('SET_ID_TOKEN', authResult.idToken);
            commit('SET_ACCESS_TOKEN', authResult.accessToken);
            commit('SET_DETAILS', extractUser(authResult.idTokenPayload));
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
