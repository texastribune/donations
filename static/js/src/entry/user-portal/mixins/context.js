export default {
  computed: {
    context() {
      const { hasError, isFetching } = this.$store.state.context;

      return {
        setError: payload => {
          this.$store.dispatch('context/setError', payload);
        },
        setIsFetching: payload => {
          this.$store.dispatch('context/setIsFetching', payload);
        },
        hasError,
        isFetching,
      };
    },
  },
};
