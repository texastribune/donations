<template>
  <summary-box heading="membership">
    <template #content>
      <p v-if="nextTransaction.card" class="has-text-gray-dark has-l-btm-marg">
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
      <p>Please note that this information does not reflect any business memberships or other sponsorships.</p>
    </template>

    <template #links>
      <user-internal-nav
        show-donation-history
        show-update-card
        show-membership-status
      >
        <template #membership-text> More about your membership </template>
      </user-internal-nav>
    </template>

    <template #bottom>
      <contact-us is-membership :display="{ size: 's' }">
        <template #text> To update your membership, contact us at </template>
      </contact-us>
    </template>
  </summary-box>
</template>

<script>
import SummaryBox from '../../../components/SummaryBox.vue';
import ContactUs from '../../../components/ContactUsSmall.vue';

export default {
  name: 'SummaryRecurringOrCircle',

  components: { SummaryBox, ContactUs },

  props: {
    nextTransaction: {
      type: Object,
      required: true,
    },
  },
};
</script>
