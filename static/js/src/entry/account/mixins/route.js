import { TITLE_SUFFIX } from '../constants';

export default {
  mounted() {
    this.setTitle();
  },

  methods: {
    setTitle() {
      document.title = `${this.$route.meta.title} ${TITLE_SUFFIX}`;
    },
  },
};
