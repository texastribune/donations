import { mapState, mapActions } from 'vuex';

export default {
  computed: {
    ...mapState('user', { user: 'details' }),
  },

  methods: {
    ...mapActions('user', ['getUser', 'getOtherUser']),
  },
};
