export default {
  props: {
    baseClasses: {
      type: [String, Array],
      default: '',
    },
  },

  computed: {
    classes() {
      const { baseClasses } = this;
      if (!baseClasses) return false;

      if (typeof baseClasses === 'string') {
        return baseClasses;
      }
      if (Array.isArray(baseClasses)) {
        return baseClasses.join(' ');
      }
      return '';
    },
  },

  methods: {
    getClasses({ obj = this, elName = 'base' }) {
      const { [`${elName}Classes`]: classes } = obj;

      if (classes) {
        if (typeof classes === 'string') {
          return classes;
        }
        if (Array.isArray(classes)) {
          return classes.join(' ');
        }
        return '';
      }
      return '';
    },
  },
};
