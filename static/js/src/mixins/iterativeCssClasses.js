export default {
  methods: {
    getClasses(elType, obj) {
      const { [`${elType}CssClasses`]: classes } = obj;

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
