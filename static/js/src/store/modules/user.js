function createDefaultState() {
  return {};
}

const mutations = {
  FOO(state) {},
};

const actions = {
  fooBar({ commit }) {
    commit('FOO');
  },
};

const getters = {
  valueByKey: state => key => state[key].value,
};

export default {
  namespaced: true,
  state: createDefaultState(),
  mutations,
  actions,
  getters,
};
