<template>
  <user-internal-nav
    show-membership-status
    show-become-sustaining
    show-renew-membership
  >
    <template #items>
      <tax-receipt :ga-label="ga.userPortal.labels.payments" />
    </template>
  </user-internal-nav>
</template>

<script>
import TaxReceipt from '../../../tax-receipt/components/LinkListItem.vue';

export default {
  name: 'PaymentsInternalNav',

  components: { TaxReceipt },
};
</script>
