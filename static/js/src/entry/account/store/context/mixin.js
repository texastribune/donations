const MODULE = 'context';

export default {
  computed: {
    contextState() {
      return this.$store.state[MODULE];
    },

    contextActions() {
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

    context() {
      return { ...this.contextActions, ...this.contextState };
    },
  },
};
