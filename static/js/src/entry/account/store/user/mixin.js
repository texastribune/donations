import { mapState, mapActions } from 'vuex';

export default {
  computed: {
    ...mapState('user', {
      user: 'details',
      userIsFetching: 'isFetching',
    }),
  },

  methods: {
    ...mapActions('user', ['getUser', 'getOtherUser']),
  },
};
