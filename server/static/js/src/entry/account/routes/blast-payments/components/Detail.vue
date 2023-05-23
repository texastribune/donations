<template>
  <user-provider v-slot="{ user: { pastBlastTransactions } }">
    <payment-list
      :payments="pastBlastTransactions"
      show-receipts
      @buildReceipt="buildReceipt"
    />
  </user-provider>
</template>

<script>
import UserProvider from '../../../store/user/Provider.vue';

import PaymentList from '../../../components/PaymentList.vue';

export default {
  name: 'BlastPaymentsDetail',

  components: { PaymentList, UserProvider },

  methods: {
    async buildReceipt({ date, amount, card }) {
      try {
        const buildBlastReceipt = await import(/* webpackChunkName: 'build-blast-receipt' */ '../build-blast-receipt');
        await buildBlastReceipt.default({
          date,
          amount,
          card,
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
