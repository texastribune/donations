import { mapState, mapActions } from 'vuex';

export default {
  computed: {
    ...mapState('context', ['appIsFetching']),
  },

  methods: {
    ...mapActions('context', ['setAppIsFetching']),
  },
};
