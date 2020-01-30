import { mapActions } from 'vuex';

import { CONTEXT_TYPES, CONTEXT_MODULE } from '../types';

export const MODULE = CONTEXT_MODULE;

const TYPES = CONTEXT_TYPES;

export default {
  computed: {
    [`${MODULE}State`]() {
      return this.$store.state[MODULE];
    },

    [MODULE]() {
      const { [`${MODULE}State`]: state } = this;

      return { ...state };
    },
  },

  methods: {
    ...mapActions(MODULE, Object.keys(TYPES).map(type => TYPES[type])),
  },
};
