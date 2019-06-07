import { mapState } from 'vuex';

import { logIn } from '../utils/auth-actions';

export default {
  data() {
    return { unauthorizedFetch: false };
  },

  created() {
    if (!this.accessToken) {
      this.unauthorizedFetch = true;
      logIn();
    }
  },

  computed: {
    ...mapState('user', ['accessToken']),
  },
};
