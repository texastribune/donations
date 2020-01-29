import { CONTEXT_MODULE } from '../../constants';

export const MODULE = CONTEXT_MODULE;

export default {
  computed: {
    [`${MODULE}State`]() {
      return this.$store.state[MODULE];
    },

    [`${MODULE}Actions`]() {
      const userActions = {
        setIsViewingAs: () => {
          this.$store.dispatch(`${MODULE}/setIsViewingAs`);
        },
        setIsFetching: () => {
          this.$store.dispatch(`${MODULE}/setIsFetching`);
        },
        setError: () => {
          this.$store.dispatch(`${MODULE}/setError`);
        },
      };

      return userActions;
    },

    [MODULE]() {
      const { [`${MODULE}Actions`]: actions, [`${MODULE}State`]: state } = this;

      return { ...actions, ...state };
    },
  },
};
