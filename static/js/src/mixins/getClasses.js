export default {
  props: {
    baseClasses: {
      type: [String, Array],
      default: '',
    },
  },

  methods: {
    getClasses(prefix = 'base', obj = this) {
      const { [`${prefix}Classes`]: classes } = obj;

      if (classes) {
        if (typeof classes === 'string') {
          return classes;
        } else if (Array.isArray(classes)) {
          return classes.join(' ');
        }
      }
      return '';
    },
  },
};
