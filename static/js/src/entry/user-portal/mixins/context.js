import { mapActions } from 'vuex';

export default {
  computed: {
    context() {
      const { hasError } = this.$store.state.context;
      return { hasError };
    },
  },

  methods: {
    ...mapActions('context', ['setError']),
  },
};
