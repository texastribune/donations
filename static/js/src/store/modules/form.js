/* eslint-disable no-param-reassign */

import Vue from 'vue';

const mutations = {
  UPDATE(state, { key, value }) {
    Object.assign(state, { [key]: value });
    Vue.set(state, key, value);
  },

  CREATE(state, initialState) {
    Object.keys(initialState).forEach((key) => {
      Vue.set(state, key, initialState[key]);
    });
  },
};

const actions = {
  updateStoreValue({ commit }, { key, value }) {
    commit('UPDATE', { key, value });
  },

  createInitialState({ commit }, initialState) {
    commit('CREATE', initialState);
  },
};

const getters = {
  storeValue: state => key => state[key],
};

export default {
  namespaced: true,
  state: {},
  mutations,
  actions,
  getters,
};
