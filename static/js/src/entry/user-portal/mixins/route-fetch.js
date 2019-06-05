export default {
  data() {
    return {
      isFetching: true,
    };
  },

  async created() {
    try {
      await this.fetchData();
    } catch (err) {
      this.setError(true);
    } finally {
      this.isFetching = false;
    }
  },
};
