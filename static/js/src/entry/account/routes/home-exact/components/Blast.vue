<template>
  <summary-box heading="the blast" :display="{ isExpired: false }">
    <template v-slot:content>
      <p
        v-if="nextTransaction.last4"
        class="has-text-gray-dark t-space-heading-m"
      >
        Your subscription to The Blast will renew on
        <strong>{{ nextTransaction.date }}</strong
        >, charging <strong>{{ nextTransaction.amount | currency }}</strong> to
        your card ending in <strong>{{ nextTransaction.last4 }}</strong
        >.
      </p>
      <p v-else class="has-text-gray-dark t-space-heading-m">
        Your subscription to The Blast is good through
        <strong>{{ nextTransaction.date }}</strong
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
    <template v-slot:bottom>
      <p class="has-text-gray-dark t-space-heading-m t-linkstyle--underlined">
        To update your subscription to The Blast, contact us at
        <a href="mailto:community@texastribune.org"
          >community@texastribune.org</a
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
