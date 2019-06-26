import { mapState } from 'vuex';

export default {
  computed: {
    ...mapState('tokenUser', {
      tokenUser: 'details',
      accessToken: 'accessToken',
    }),
  },
};
