import { mapState, mapGetters } from 'vuex';

export default {
  computed: {
    ...mapState('tokenUser', {
      tokenUser: 'details',
      canViewAs: 'canViewAs',
      isVerified: 'isVerified',
      tokenUserError: 'error',
    }),

    ...mapGetters('tokenUser', ['isLoggedIn']),
  },
};
