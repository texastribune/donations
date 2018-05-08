export default {
  props: {
    cssClasses: {
      type: [String, Array],
      default: '',
    },
  },

  computed: {
    classes() {
      const { cssClasses } = this;

      if (cssClasses) {
        if (typeof classes === 'string') {
          return cssClasses;
        } else if (Array.isArray(cssClasses)) {
          return cssClasses.join(' ');
        }
      }
      return '';
    },
  },
};
