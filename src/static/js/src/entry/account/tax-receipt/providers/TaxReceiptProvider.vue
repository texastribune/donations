<script>
import userMixin from '../../store/user/mixin';

export default {
  name: 'TaxReceiptProvider',

  mixins: [userMixin],

  methods: {
    async buildReceipt(gaLabel) {
      try {
        const buildTaxReceipt = await import(/* webpackChunkName: 'build-tax-receipt' */ '../build-tax-receipt');
        const { lastYearAmount, greeting } = this.user;
        const { lastYear } = this.dates;

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
    const { buildReceipt } = this;

    return this.$scopedSlots.default({
      taxReceipt: { buildReceipt },
    });
  },
};
</script>
