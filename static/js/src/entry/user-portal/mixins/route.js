import contextMixin from './context';
import { TITLE_SUFFIX } from '../constants';

export default {
  mixins: [contextMixin],

  created() {
    this.setTitle();
  },

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

  methods: {
    setTitle() {
      document.title = `${this.$route.meta.title} ${TITLE_SUFFIX}`;
    },
  },
};
