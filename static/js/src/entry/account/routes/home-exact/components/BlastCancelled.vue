<template>
  <summary-box heading="the blast" :display="{ isExpired: false }">
    <template v-slot:content>
      <p
        v-if="lastTransaction.last4"
        class="has-text-gray-dark t-space-heading-m"
      >
        Your subscription to The Blast is no longer active. Your last payment of
        <strong>{{ lastTransaction.amount | currency }}</strong> was charged to
        your card ending in <strong>{{ lastTransaction.last4 }}</strong> on
        <strong>{{ lastTransaction.date | longDate }}</strong
        >.
      </p>
      <p v-else class="has-text-gray-dark t-space-heading-m">
        Your subscription to The Blast is no longer active. Your last payment of
        <strong>{{ lastTransaction.amount | currency }}</strong> was made on
        <strong>{{ lastTransaction.date | longDate }}</strong
        >.
      </p>
    </template>
    <template v-slot:links>
      <ul class="c-link-list">
        <li class="has-xs-btm-marg">
          <span class="c-link-list__arrow has-text-teal">
            <strong>&rarr;</strong>
          </span>
          <span class="has-text-gray-dark">
            <a
              href="/blastform"
              ga-on="click"
              :ga-event-category="ga.blastIntent.category"
              :ga-event-action="ga.blastIntent.actions['renew-blast']"
              :ga-event-label="ga.blastIntent.labels['user-portal']"
            >
              Renew your subscription to The Blast
            </a>
          </span>
        </li>
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
  </summary-box>
</template>

<script>
import SummaryBox from '../../../components/SummaryBox.vue';

export default {
  name: 'BlastCancelled',

  components: { SummaryBox },

  props: {
    lastTransaction: {
      type: Object,
      required: true,
    },
  },
};
</script>
