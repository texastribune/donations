import { TITLE_SUFFIX } from '../constants';

export default {
  created() {
    this.setTitle();
  },

  methods: {
    setTitle() {
      document.title = `${this.$route.meta.title} ${TITLE_SUFFIX}`;
    },
  },
};
