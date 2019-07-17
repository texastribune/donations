import { mapState } from 'vuex';

export default {
  computed: {
    ...mapState('tokenUser', {
      tokenUser: 'details',
      accessToken: 'accessToken',
      canViewAs: 'canViewAs',
      isVerified: 'isVerified',
      tokenUserError: 'error',
    }),
  },
};
