export default {
  computed: {
    userActions() {
      return this.$store.user.actions;
    },

    userGetters() {
      return this.$store.user.getters;
    },

    user() {
      const { userGetters, userActions } = this;

      return { ...userGetters, ...userActions };
    },
  },
};
