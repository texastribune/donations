import { mapActions } from 'vuex';

import { USER_TYPES, USER_MODULE } from '../types';

export const MODULE = USER_MODULE;
const TYPES = USER_TYPES;

export default {
  computed: {
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
      const { [`${MODULE}Getters`]: getters } = this;

      return { ...getters };
    },
  },

  methods: {
    ...mapActions(MODULE, Object.keys(TYPES).map(type => TYPES[type])),
  },
};
