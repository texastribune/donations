<template>
  <summary-box heading="membership">
    <template #content>
      <p v-if="lastTransaction.card" class="has-text-gray-dark has-l-btm-marg">
        Thank you for being a Texas Tribune member! Your last donation of
        <strong>{{ lastTransaction.amount | currency }}</strong> was charged on
        <strong>{{ lastTransaction.date | longDate }}</strong
        >, to your card ending in
        <strong>{{ lastTransaction.card.last4 }}</strong
        >. Your membership is good through
        <strong>{{ membershipExpirationDate | longDate }}</strong
        >.
      </p>
      <p v-else class="has-text-gray-dark">
        Thank you for being a Texas Tribune member! Your last donation of
        <strong>{{ lastTransaction.amount | currency }}</strong> was on
        <strong>{{ lastTransaction.date | longDate }}</strong
        >. Your membership is good through
        <strong>{{ membershipExpirationDate | longDate }}</strong
        >.
      </p>
      <p>Please note that this information does not reflect any business memberships or other sponsorships.</p>
    </template>

    <template #links>
      <user-internal-nav
        show-donation-history
        show-membership-status
        show-become-sustaining
      >
        <template #membership-text> More about your membership </template>
      </user-internal-nav>
    </template>
  </summary-box>
</template>

<script>
import SummaryBox from '../../../components/SummaryBox.vue';

export default {
  name: 'SummarySingleOrWillExpire',

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
