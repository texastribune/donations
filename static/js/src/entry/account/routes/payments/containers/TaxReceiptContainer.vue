<template>
  <tax-receipt
    v-if="receiptAmount > 0"
    :greeting="greeting"
    :receipt-amount="receiptAmount"
  />
</template>

<script>
import userMixin from '../../../store/user/mixin';
import TaxReceipt from '../components/TaxReceipt.vue';

export default {
  name: 'TaxReceiptContainer',

  components: { TaxReceipt },

  mixins: [userMixin],

  computed: {
    receiptAmount() {
      return this.user.total_gifts_last_year;
    },

    greeting() {
      return this.user.greeting;
    },
  },
};
</script>
