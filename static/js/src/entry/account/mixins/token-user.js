import { mapState } from 'vuex';

export default {
  computed: {
    ...mapState('user', { tokenUser: 'tokenDetails' }),
  },
};
