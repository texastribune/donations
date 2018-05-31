/* eslint-disable no-param-reassign */

import Vue from 'vue';

const mutations = {
  UPDATE(state, { key, value }) {
    Vue.set(state, key, value);
  },

  CREATE(state, initialState) {
    Object.keys(initialState).forEach((key) => {
      Vue.set(state, key, initialState[key]);
    });
  },
};

const actions = {
  updateValue({ commit }, { key, value }) {
    commit('UPDATE', { key, value });
  },

  updateValues({ commit }, updates) {
    Object.keys(updates).forEach((key) => {
      commit('UPDATE', { key, value: updates[key] });
    });
  },

  createInitialState({ commit }, initialState) {
    commit('CREATE', initialState);
  },
};

const getters = {
  valueByKey: state => key => state[key],
};

export default {
  namespaced: true,
  state: {},
  mutations,
  actions,
  getters,
};
