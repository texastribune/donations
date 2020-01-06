<template>
  <user-internal-nav
    show-membership-status
    show-become-sustaining
    show-renew-membership
  >
    <template v-slot:items>
      <tax-receipt />
    </template>
  </user-internal-nav>
</template>

<script>
import TaxReceipt from '../containers/TaxReceiptContainer.vue';

export default {
  name: 'PaymentsInternalNav',

  components: { TaxReceipt },
};
</script>
