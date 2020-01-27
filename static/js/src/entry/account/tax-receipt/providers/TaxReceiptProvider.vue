<script>
import getYear from 'date-fns/get_year';

import userMixin from '../../store/user/mixin';

export default {
  name: 'TaxReceiptProvider',

  mixins: [userMixin],

  computed: {
    lastYear() {
      return getYear(new Date()) - 1;
    },
  },

  methods: {
    async buildReceipt(gaLabel) {
      try {
        const buildTaxReceipt = await import(/* webpackChunkName: 'build-tax-receipt' */ '../build-tax-receipt');
        const { lastYear, user } = this;
        const { lastYearAmount, greeting } = user;

        await buildTaxReceipt.default({
          lastYear,
          lastYearAmount,
          greeting,
        });
      } finally {
        window.dataLayer.push({
          event: this.ga.customEventName,
          gaCategory: this.ga.userPortal.category,
          gaAction: this.ga.userPortal.actions['tax-receipt'],
          gaLabel,
        });
      }
    },
  },

  render() {
    const { buildReceipt, lastYear } = this;

    return this.$scopedSlots.default({
      taxReceipt: { buildReceipt, lastYear },
    });
  },
};
</script>
