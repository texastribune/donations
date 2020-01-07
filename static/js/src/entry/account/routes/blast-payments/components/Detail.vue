<template>
  <payment-list :payments="data" show-receipts @buildReceipt="buildReceipt" />
</template>

<script>
import PaymentList from '../../../components/PaymentList.vue';

export default {
  name: 'BlastPaymentsDetail',

  components: { PaymentList },

  props: {
    data: {
      type: Array,
      required: true,
    },
  },

  methods: {
    async buildReceipt({ date, amount, method }) {
      try {
        const buildBlastReceipt = await import(/* webpackChunkName: 'build-blast-receipt' */ '../build-blast-receipt');
        await buildBlastReceipt.default({
          date,
          amount,
          method,
        });
      } finally {
        window.dataLayer.push({
          event: this.ga.customEventName,
          gaCategory: this.ga.userPortal.category,
          gaAction: this.ga.userPortal.actions['blast-receipt'],
          gaLabel: this.ga.userPortal.labels['blast-payments'],
        });
      }
    },
  },
};
</script>
