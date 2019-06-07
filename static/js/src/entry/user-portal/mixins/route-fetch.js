import { mapActions } from 'vuex';

export default {
  data() {
    return {
      isFetching: true,
    };
  },

  async created() {
    if (!this.unauthorizedFetch) {
      try {
        await this.fetchData();
      } catch (err) {
        this.setError(true);
      } finally {
        this.isFetching = false;
      }
    }
  },

  methods: {
    ...mapActions('context', ['setError']),
  },
};
