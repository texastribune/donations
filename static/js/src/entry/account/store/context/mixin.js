import { mapActions } from 'vuex';

import { CONTEXT_TYPES, CONTEXT_MODULE } from '../types';

export const MODULE = CONTEXT_MODULE;
const TYPES = CONTEXT_TYPES;

export default {
  computed: {
    [`${MODULE}State`]() {
      return this.$store.state[MODULE];
    },

    [`${MODULE}Getters`]() {
      const relevantGetters = {};
      const allGetters = this.$store.getters;

      Object.keys(allGetters).forEach(getterName => {
        if (getterName.indexOf(`${MODULE}/`) !== -1) {
          relevantGetters[getterName.replace(`${MODULE}/`, '')] =
            allGetters[getterName];
        }
      });

      return relevantGetters;
    },

    [MODULE]() {
      const { [`${MODULE}State`]: state, [`${MODULE}Getters`]: getters } = this;

      return { ...state, ...getters };
    },
  },

  methods: {
    ...mapActions(MODULE, Object.keys(TYPES).map(type => TYPES[type])),
  },
};
