<template>
  <tax-receipt-provider v-slot="{ buildReceipt, lastYear }">
    <link-list-item>
      <template v-slot:main>
        <button class="c-link-button" @click="buildReceipt(taxReceiptGaLabel)">
          Download your {{ lastYear }} tax receipt
        </button>
      </template>
    </link-list-item>
  </tax-receipt-provider>
</template>

<script>
import LinkListItem from '../../components/LinkListItem.vue';
import TaxReceiptProvider from '../providers/TaxReceiptProvider.vue';

export default {
  name: 'LinkListItemTaxReceipt',

  components: { LinkListItem, TaxReceiptProvider },

  props: {
    taxReceiptGaLabel: {
      type: String,
      required: true,
    },
  },
};
</script>
