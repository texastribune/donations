<template>
  <summary-box heading="membership" :display="{ isExpired: true }">
    <template #content>
      <p class="has-text-gray-dark">
        Thanks for your previous support!
        <span class="has-text-error"
          >Your membership expired on
          <strong>{{ membershipExpirationDate | longDate }}</strong
          >.</span
        >
        <template v-if="lastTransaction.card">
          Your last donation of
          <strong>{{ lastTransaction.amount | currency }}</strong> was charged
          on <strong>{{ lastTransaction.date | longDate }}</strong
          >, to your card ending in
          <strong>{{ lastTransaction.card.last4 }}</strong
          >.
        </template>
        <template v-else>
          Your last donation of
          <strong>{{ lastTransaction.amount | currency }}</strong> was on
          <strong>{{ lastTransaction.date | longDate }}</strong
          >.
        </template>
      </p>
    </template>

    <template #links>
      <user-internal-nav
        show-donation-history
        show-membership-status
        show-renew-membership
      >
        <template #membership-text> More about your membership </template>
      </user-internal-nav>
    </template>
  </summary-box>
</template>

<script>
import SummaryBox from '../../../components/SummaryBox.vue';

export default {
  name: 'SummaryExpired',

  components: { SummaryBox },

  props: {
    lastTransaction: {
      type: Object,
      required: true,
    },

    membershipExpirationDate: {
      type: String,
      required: true,
    },
  },
};
</script>
