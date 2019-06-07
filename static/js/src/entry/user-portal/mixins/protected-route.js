import { mapState } from 'vuex';

import { logIn } from '../utils/auth-actions';

export default {
  created() {
    if (!this.accessToken) logIn();
  },

  computed: {
    ...mapState('user', ['accessToken']),
  },
};
