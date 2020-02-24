<template>
  <summary-box heading="membership">
    <template v-slot:content>
      <p v-if="nextTransaction.card" class="has-text-gray-dark">
        Thank you for being a Texas Tribune member! Your next
        <strong>{{ nextTransaction.period }}</strong> donation of
        <strong>{{ nextTransaction.amount | currency }}</strong> will be charged
        on <strong>{{ nextTransaction.date | longDate }}</strong
        >, to your card ending in
        <strong>{{ nextTransaction.card.last4 }}</strong
        >.
      </p>
      <p v-else class="has-text-gray-dark">
        Thank you for being a Texas Tribune member! Your next
        {{ nextTransaction.period }} donation of
        <strong>{{ nextTransaction.amount | currency }}</strong> is due on
        <strong>{{ nextTransaction.date | longDate }}</strong
        >.
      </p>
    </template>

    <template v-slot:links>
      <user-internal-nav
        show-donation-history
        show-membership-status
        show-ambassador
      >
        <template v-slot:membership-text>
          More about your membership
        </template>
      </user-internal-nav>
    </template>

    <template v-slot:bottom>
      <p class="has-text-gray-dark t-links-underlined">
        To update your membership, contact us at
        <a
          href="mailto:membership@texastribune.org"
          ga-on="click"
          :ga-event-category="ga.donations.category"
          :ga-event-action="ga.donations.actions['membership-intent']"
          :ga-event-label="ga.donations.labels['upgrade-contact']"
        >
          membership@texastribune.org</a
        >.
      </p>
    </template>
  </summary-box>
</template>

<script>
import SummaryBox from '../../../components/SummaryBox.vue';

export default {
  name: 'SummaryRecurringOrCircle',

  components: { SummaryBox },

  props: {
    nextTransaction: {
      type: Object,
      required: true,
    },
  },
};
</script>
