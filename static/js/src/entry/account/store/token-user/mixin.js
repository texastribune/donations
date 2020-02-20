import { TOKEN_USER_MODULE } from '../types';

export const MODULE = TOKEN_USER_MODULE;

export default {
  computed: {
    [`${MODULE}Getters`]() {
      const tokenUserGetters = {};
      const allGetters = this.$store.getters;

      Object.keys(allGetters).forEach(getterName => {
        if (getterName.indexOf(`${MODULE}/`) !== -1) {
          tokenUserGetters[getterName.replace(`${MODULE}/`, '')] =
            allGetters[getterName];
        }
      });

      return tokenUserGetters;
    },

    [`${MODULE}State`]() {
      const { error, isLoggedIn } = this.$store.state[MODULE];
      return { error, isLoggedIn };
    },

    [MODULE]() {
      const { [`${MODULE}Getters`]: getters, [`${MODULE}State`]: state } = this;

      return { ...getters, ...state };
    },
  },
};
