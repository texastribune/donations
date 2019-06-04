import { mapActions } from 'vuex';

export default {
  async created() {
    this.setIsFetching(true);

    try {
      await this.fetchData();
    } catch (err) {
      this.setError(true);
    }

    this.setIsFetching(false);
  },

  methods: {
    ...mapActions('context', ['setIsFetching', 'setError']),
  },
};
