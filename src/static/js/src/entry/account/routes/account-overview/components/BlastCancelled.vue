<template>
  <summary-box heading="the blast">
    <template #content>
      <p v-if="lastTransaction.card" class="has-text-gray-dark">
        Your subscription to The Blast is no longer active. Your last payment of
        <strong>{{ lastTransaction.amount | currency }}</strong> was charged to
        your card ending in <strong>{{ lastTransaction.card.last4 }}</strong> on
        <strong>{{ lastTransaction.date | longDate }}</strong
        >.
      </p>
      <p v-else class="has-text-gray-dark">
        Your subscription to The Blast is no longer active. Your last payment of
        <strong>{{ lastTransaction.amount | currency }}</strong> was made on
        <strong>{{ lastTransaction.date | longDate }}</strong
        >.
      </p>
    </template>

    <template #links>
      <user-internal-nav show-renew-blast show-blast-payments />
    </template>
  </summary-box>
</template>

<script>
import SummaryBox from '../../../components/SummaryBox.vue';

export default {
  name: 'SummaryBlastCancelled',

  components: { SummaryBox },

  props: {
    lastTransaction: {
      type: Object,
      required: true,
    },
  },
};
</script>
