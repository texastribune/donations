/* eslint-disable no-param-reassign */

// import axios from 'axios';

import auth from '../../utils/auth';
import { setFlag, clearFlag, isLoggedIn } from '../../utils/auth-actions';
import { LoggedOutError, Auth0Error } from '../../errors';
// import { PORTAL_API_URL } from '../../constants';

import response from '../../dummy/recurring.json';
// import response from '../../dummy/one_time.json';
// import response from '../../dummy/never_given.json';
// import response from '../../dummy/recurring_expired_and_blast.json';

function createDefaultState() {
  return {
    accessToken: '',
    tokenDetails: {},
    details: {},
  };
}

const mutations = {
  SET_ACCESS_TOKEN(state, accessToken) {
    state.accessToken = accessToken;
  },

  SET_TOKEN_DETAILS(state, tokenDetails) {
    state.tokenDetails = tokenDetails;
  },

  SET_DETAILS(state, details) {
    state.details = details;
  },
};

const actions = {
  getUser: async ({ commit }) => {
    /* await axios.get(PORTAL_API_URL, {
      headers: { Authorization: `Bearer ${state.accessToken}` },
    }); */

    // commit('SET_DETAILS', data);
    commit('SET_DETAILS', response);
  },

  getTokenUser: ({ commit }) =>
    new Promise((resolve, reject) => {
      if (isLoggedIn()) {
        auth.checkSession(
          { responseType: 'token id_token' },
          (err, authResult) => {
            if (err && err.error === 'login_required') {
              clearFlag();
              return reject(new LoggedOutError());
            }
            if (
              err ||
              !authResult ||
              !authResult.accessToken ||
              !authResult.idTokenPayload
            ) {
              clearFlag();
              return reject(new Auth0Error());
            }

            commit('SET_ACCESS_TOKEN', authResult.accessToken);
            commit('SET_TOKEN_DETAILS', authResult.idTokenPayload);
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
