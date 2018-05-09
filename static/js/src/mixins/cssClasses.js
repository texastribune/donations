export default {
  props: {
    baseCssClasses: {
      type: [String, Array],
      default: '',
    },
  },

  methods: {
    getCssClasses(elName = 'base', obj = this) {
      const { [`${elName}CssClasses`]: classes } = obj;

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
