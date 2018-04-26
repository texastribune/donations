/* eslint-disable no-param-reassign */

const mutations = {
  UPDATE(state, { key, value }) {
    Object.assign(state, { [key]: value });
  },

  CREATE(state, initialState) {
    Object.assign(state, initialState);
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
