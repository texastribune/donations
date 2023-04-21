<template>
  <tax-receipt-provider v-slot="{ taxReceipt: { buildReceipt } }">
    <link-list-item>
      <template #main>
        <button class="c-link-button" @click="buildReceipt(gaLabel)">
          Download your {{ dates.lastYear }} tax receipt
        </button>
      </template>
    </link-list-item>
  </tax-receipt-provider>
</template>

<script>
import TaxReceiptProvider from '../providers/TaxReceiptProvider.vue';

import LinkListItem from '../../components/LinkListItem.vue';

export default {
  name: 'LinkListItemTaxReceipt',

  components: { LinkListItem, TaxReceiptProvider },

  props: {
    gaLabel: {
      type: String,
      required: true,
    },
  },
};
</script>
