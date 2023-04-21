import Vue from 'vue';

const mutations = {
  UPDATE_VALUE(state, { key, value }) {
    Vue.set(state[key], 'value', value);
  },

  UPDATE_VALIDITY(state, { key, isValid }) {
    Vue.set(state[key], 'isValid', isValid);
  },

  CREATE(state, initialState) {
    Object.keys(initialState).forEach(key => {
      Vue.set(state, key, initialState[key]);
    });
  },
};

const actions = {
  updateValue({ commit }, { key, value }) {
    commit('UPDATE_VALUE', { key, value });
  },

  updateValues({ commit }, updates) {
    Object.keys(updates).forEach(key => {
      commit('UPDATE_VALUE', { key, value: updates[key] });
    });
  },

  updateValidity({ commit }, { key, isValid }) {
    commit('UPDATE_VALIDITY', { key, isValid });
  },

  createInitialState({ commit }, initialState) {
    commit('CREATE', initialState);
  },
};

const getters = {
  valueByKey: state => key => state[key].value,
  validityByKey: state => key => state[key].isValid,
  validatorByKey: state => key => state[key].validator,
  messageByKey: state => key => state[key].message,
};

export default {
  namespaced: true,
  state: {},
  mutations,
  actions,
  getters,
};
