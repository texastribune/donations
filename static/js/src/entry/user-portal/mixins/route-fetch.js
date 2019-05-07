import contextMixin from './context';

export default {
  mixins: [contextMixin],

  beforeMount() {
    this.context.setIsFetching(true);
  },

  async mounted() {
    try {
      await this.fetchData();
    } catch (err) {
      this.context.setError(true);
    }

    this.context.setIsFetching(false);
  },
};
