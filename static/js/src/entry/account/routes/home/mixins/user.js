import { mapState } from 'vuex';

export default {
  computed: {
    ...mapState('user', { user: 'details' }),
  },
};
