import { USER_MODULE } from '../../constants';

export const MODULE = USER_MODULE;

export default {
  computed: {
    [`${MODULE}Getters`]() {
      const relevantGetters = {};
      const allGetters = this.$store.getters;

      Object.keys(allGetters).forEach(getterName => {
        if (getterName.indexOf(`${MODULE}/`) !== -1) {
          relevantGetters[getterName.replace(`${MODULE}/`, '')] =
            allGetters[getterName];
        }
      });

      return relevantGetters;
    },

    [`${MODULE}Actions`]() {
      const relevantActions = {
        getViewAsUser: () => {
          this.$store.dispatch(`${MODULE}/getViewAsUser`);
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

      return relevantActions;
    },

    [MODULE]() {
      const {
        [`${MODULE}Getters`]: getters,
        [`${MODULE}Actions`]: actions,
      } = this;

      return { ...getters, ...actions };
    },
  },
};
