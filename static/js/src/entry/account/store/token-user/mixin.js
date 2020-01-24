const MODULE = 'tokenUser';

export default {
  computed: {
    tokenUserGetters() {
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

    tokenUserState() {
      const { error } = this.$store.state[MODULE];

      return { error };
    },

    tokenUser() {
      return { ...this.tokenUserGetters, ...this.tokenUserState };
    },
  },
};
