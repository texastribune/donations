<template>
  <summary-box heading="the blast" :display="{ isExpired: false }">
    <template v-slot:content>
      <p
        v-if="lastTransaction.last4"
        class="has-text-gray-dark t-space-heading-m"
      >
        Your subscription to The Blast was cancelled. Your last payment of
        <strong>${{ lastTransaction.amount }}</strong> was charged to your card
        ending in <strong>{{ lastTransaction.last4 }}</strong> on
        <strong>{{ lastTransaction.date }}</strong
        >.
      </p>
      <p v-else class="has-text-gray-dark t-space-heading-m">
        Your subscription to The Blast was cancelled. Your last payment of
        <strong>${{ lastTransaction.amount }}</strong> was on
        <strong>{{ lastTransaction.date }}</strong
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
            <a href="/blastform">Renew your subscription to The Blast</a>
          </span>
        </li>
        <li>
          <span class="c-link-list__arrow has-text-teal">
            <strong>&rarr;</strong>
          </span>
          <span class="has-text-gray-dark">
            <router-link :to="{ name: 'blast-payments' }"
              >See your payment history</router-link
            >
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
