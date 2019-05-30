import contextMixin from './context';

export default {
  mixins: [contextMixin],

  async created() {
    this.context.setIsFetching(true);

    try {
      await this.fetchData();
    } catch (err) {
      this.context.setError(true);
    }

    this.context.setIsFetching(false);
  },
};
