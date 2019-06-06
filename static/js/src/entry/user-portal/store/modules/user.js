/* eslint-disable no-param-reassign */

import axios from 'axios';

import { PORTAL_API_URL } from '../../constants';
import auth from '../../utils/auth';
import { setFlag, clearFlag, isLoggedIn } from '../../utils/auth-actions';
import { LoggedOutError, Auth0Error } from '../../errors';

// import response from '../../dummy/recurring.json';
// import response from '../../dummy/one_time.json';
// import response from '../../dummy/never_given.json';
import response from '../../dummy/recurring_expired_and_blast.json';

function createDefaultState() {
  return {
    accessToken: '',
    details: {},
  };
}

const mutations = {
  SET_ACCESS_TOKEN(state, accessToken) {
    state.accessToken = accessToken;
  },

  SET_DETAILS(state, details) {
    state.details = details;
  },
};

const actions = {
  getUser: async ({ commit, state }) => {
    /* const { data } = await axios.get(PORTAL_API_URL, {
      headers: { Authorization: `Bearer ${state.accessToken}` },
    }); */

    // commit('SET_DETAILS', data);
    commit('SET_DETAILS', response);
  },

  getToken: ({ commit }) =>
    new Promise((resolve, reject) => {
      if (isLoggedIn()) {
        auth.checkSession({ responseType: 'token' }, (err, authResult) => {
          if (err && err.error === 'login_required') {
            clearFlag();
            return reject(new LoggedOutError());
          }
          if (err || !authResult || !authResult.accessToken) {
            clearFlag();
            return reject(new Auth0Error());
          }

          commit('SET_ACCESS_TOKEN', authResult.accessToken);
          setFlag();
          return resolve();
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
