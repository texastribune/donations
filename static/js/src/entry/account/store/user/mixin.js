const MODULE = 'user';

export default {
  computed: {
    userGetters() {
      const userGetters = {};
      const allGetters = this.$store.getters;

      Object.keys(allGetters).forEach(getterName => {
        if (getterName.indexOf(`${MODULE}/`) !== -1) {
          userGetters[getterName.replace(`${MODULE}/`, '')] =
            allGetters[getterName];
        }
      });

      return userGetters;
    },

    userActions() {
      const userActions = {
        getOtherUser: () => {
          this.$store.dispatch(`${MODULE}/getOtherUser`);
        },
        getUser: () => {
          this.$store.dispatch(`${MODULE}/getUser`);
        },
        updateUser: () => {
          this.$store.dispatch(`${MODULE}/updateUser`);
        },
        updateIdentity: () => {
          this.$store.dispatch(`${MODULE}/updateIdentity`);
        },
        linkIdentity: () => {
          this.$store.dispatch(`${MODULE}/linkIdentity`);
        },
        confirmLinkedIdentity: () => {
          this.$store.dispatch(`${MODULE}/confirmLinkedIdentity`);
        },
      };

      return userActions;
    },

    user() {
      return { ...this.userGetters, ...this.userActions };
    },
  },
};
