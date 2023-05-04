<template>
  <summary-box heading="the blast">
    <template #content>
      <p v-if="nextTransaction.card" class="has-text-gray-dark">
        Thanks for subscribing to The Blast! Your next
        <strong>{{ nextTransaction.period }}</strong> payment of
        <strong>{{ nextTransaction.amount | currency }}</strong> will be charged
        on <strong>{{ nextTransaction.date | longDate }}</strong
        >, to your card ending in
        <strong>{{ nextTransaction.card.last4 }}</strong
        >.
      </p>
      <p v-else class="has-text-gray-dark t-links-underlined">
        Thanks for subscribing to The Blast! Your subscription is paid through
        <strong>{{ nextTransaction.date | longDate }}</strong
        >. To update or extend your subscription, contact us at
        <a
          href="mailto:blast@texastribune.org"
          ga-on="click"
          :ga-event-category="ga.userPortal.category"
          :ga-event-action="ga.userPortal.actions['contact-us']"
          :ga-event-label="ga.userPortal.labels.home"
        >
          blast@texastribune.org </a
        >.
      </p>
    </template>

    <template #links>
      <user-internal-nav show-blast-payments />
    </template>

    <template v-if="nextTransaction.card" #bottom>
      <contact-us
        :ga-label="ga.userPortal.labels.home"
        :display="{ size: 's' }"
        is-blast
      >
        <template #text> Need to make a change? Contact us at </template>
      </contact-us>
    </template>
  </summary-box>
</template>

<script>
import SummaryBox from '../../../components/SummaryBox.vue';
import ContactUs from '../../../components/ContactUsSmall.vue';

export default {
  name: 'SummaryBlast',

  components: { SummaryBox, ContactUs },

  props: {
    nextTransaction: {
      type: Object,
      required: true,
    },
  },
};
</script>
