import { mapState, mapActions } from 'vuex';

export default {
  computed: {
    ...mapState('context', {
      appIsFetching: 'isFetching',
      appError: 'error',
    }),
  },

  methods: {
    ...mapActions('context', {
      setAppIsFetching: 'setIsFetching',
      setAppError: 'setError',
    }),
  },
};
