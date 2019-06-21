<template>
  <summary-box heading="the blast" :display="{ isExpired: false }">
    <template v-slot:content>
      <p
        v-if="nextTransaction.last4"
        class="has-text-gray-dark t-space-heading-m"
      >
        Thanks for subscribing to The Blast! Your next
        <strong>{{ nextTransaction.period }}</strong> payment of
        <strong>{{ nextTransaction.amount | currency }}</strong> will be charged
        on <strong>{{ nextTransaction.date | longDate }}</strong
        >, to your card ending in <strong>{{ nextTransaction.last4 }}</strong
        >.
      </p>
      <p
        v-else
        class="has-text-gray-dark t-space-heading-m t-linkstyle--underlined"
      >
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
    <template v-slot:links>
      <ul class="c-link-list">
        <li>
          <span class="c-link-list__arrow has-text-teal">
            <strong>&rarr;</strong>
          </span>
          <span class="has-text-gray-dark">
            <router-link
              ga-on="click"
              :to="{ name: 'blast-payments' }"
              :ga-event-category="ga.userPortalNav.category"
              :ga-event-action="ga.userPortalNav.actions.inline"
              :ga-event-label="ga.userPortalNav.labels['blast-payments']"
            >
              See your payment history
            </router-link>
          </span>
        </li>
      </ul>
    </template>
    <template v-if="nextTransaction.last4" v-slot:bottom>
      <p class="has-text-gray-dark t-space-heading-m t-linkstyle--underlined">
        Need to make a change? Contact us at
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
  </summary-box>
</template>

<script>
import SummaryBox from '../../../components/SummaryBox.vue';

export default {
  name: 'Blast',

  components: { SummaryBox },

  props: {
    nextTransaction: {
      type: Object,
      required: true,
    },
  },
};
</script>
