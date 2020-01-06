<template>
  <internal-nav-item>
    <button class="c-link-button" @click="buildReceipt">
      Download your {{ lastYear }} tax receipt
    </button>
  </internal-nav-item>
</template>

<script>
import getYear from 'date-fns/get_year';

import InternalNavItem from '../../../nav/components/InternalNavItem.vue';

export default {
  name: 'TaxReceipt',

  components: { InternalNavItem },

  props: {
    receiptAmount: {
      type: Number,
      required: true,
    },

    greeting: {
      type: String,
      required: true,
    },
  },

  computed: {
    lastYear() {
      return getYear(new Date()) - 1;
    },
  },

  methods: {
    async buildReceipt() {
      try {
        const buildTaxReceipt = await import(/* webpackChunkName: 'build-tax-receipt' */ '../build-tax-receipt');
        const { lastYear, receiptAmount, greeting } = this;
        await buildTaxReceipt.default({
          lastYear,
          receiptAmount,
          greeting,
        });
      } finally {
        window.dataLayer.push({
          event: this.ga.customEventName,
          gaCategory: this.ga.userPortal.category,
          gaAction: this.ga.userPortal.actions['tax-receipt'],
          gaLabel: this.ga.userPortal.labels.payments,
        });
      }
    },
  },
};
</script>
