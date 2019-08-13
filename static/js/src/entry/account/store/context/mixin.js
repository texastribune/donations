import { mapState, mapActions } from 'vuex';

export default {
  computed: {
    ...mapState('context', ['appIsFetching', 'error']),
  },

  methods: {
    ...mapActions('context', ['setAppIsFetching', 'setError']),
  },
};
