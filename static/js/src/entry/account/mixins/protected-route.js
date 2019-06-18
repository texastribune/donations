import { mapState, mapActions } from 'vuex';

import { logIn, logOut } from '../utils/auth-actions';
import tokenUserMixin from './token-user';

export default {
  mixins: [tokenUserMixin],

  data() {
    return { unauthorizedFetch: false };
  },

  created() {
    if (!this.accessToken) {
      this.unauthorizedFetch = true;
      logIn();
    } else if (!this.tokenUser.email_verified) {
      this.unauthorizedFetch = true;
      this.setUnverified();
    }
  },

  computed: {
    ...mapState('user', ['accessToken']),
  },

  methods: {
    ...mapActions('context', ['setUnverified']),
  },

  watch: {
    accessToken(newToken, oldToken) {
      if (oldToken && !newToken) logOut();
    },
  },
};
