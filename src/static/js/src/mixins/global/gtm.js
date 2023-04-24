export default {
  props: {
    gtm: {
      type: [Object, Boolean],
      default: false,
    },
  },

  computed: {
    gtmOn() {
      return this.gtm ? this.gtm.on : false;
    },

    gtmLabel() {
      return this.gtm ? this.gtm.label : false;
    },

    gtmAction() {
      return this.gtm ? this.gtm.action : false;
    },

    gtmValue() {
      if (!this.gtm) return false;
      return this.gtm.value || false;
    },
  },

  methods: {
    getGtmOn({ obj = this, elName }) {
      const key = elName ? `${elName}Gtm` : 'gtm';
      return obj[key].on;
    },

    getGtmLabel({ obj = this, elName }) {
      const key = elName ? `${elName}Gtm` : 'gtm';
      return obj[key].label;
    },

    getGtmAction({ obj = this, elName }) {
      const key = elName ? `${elName}Gtm` : 'gtm';
      return obj[key].action;
    },

    getGtmValue({ obj = this, elName }) {
      const key = elName ? `${elName}Gtm` : 'gtm';
      return obj[key].value || false;
    },
  },
};
