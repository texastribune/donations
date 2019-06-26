<template>
  <summary-box heading="membership" :display="{ isExpired: false }">
    <template v-slot:content>
      <p
        v-if="lastTransaction.last4"
        class="has-text-gray-dark t-space-heading-m"
      >
        Thank you for being a Texas Tribune member! Your last donation of
        <strong>{{ lastTransaction.amount | currency }}</strong> was charged on
        <strong>{{ lastTransaction.date | longDate }}</strong
        >, to your card ending in <strong>{{ lastTransaction.last4 }}</strong
        >. Your membership is good through
        <strong>{{ membershipExpirationDate | longDate }}</strong
        >.
      </p>
      <p v-else class="has-text-gray-dark t-space-heading-m">
        Thank you for being a Texas Tribune member! Your last donation of
        <strong>{{ lastTransaction.amount | currency }}</strong> was on
        <strong>{{ lastTransaction.date | longDate }}</strong
        >. Your membership is good through
        <strong>{{ membershipExpirationDate | longDate }}</strong
        >.
      </p>
    </template>
    <template v-slot:links>
      <ul class="c-link-list">
        <li class="has-m-btm-marg">
          <span class="c-link-list__arrow has-text-teal">
            <strong>&rarr;</strong>
          </span>
          <span class="has-text-gray-dark">
            <router-link
              ga-on="click"
              :to="{ name: 'payments' }"
              :ga-event-category="ga.userPortalNav.category"
              :ga-event-action="ga.userPortalNav.actions.inline"
              :ga-event-label="ga.userPortalNav.labels.payments"
            >
              See your donation history
            </router-link>
          </span>
        </li>
        <li class="has-m-btm-marg">
          <span class="c-link-list__arrow has-text-teal">
            <strong>&rarr;</strong>
          </span>
          <span class="has-text-gray-dark">
            <router-link
              ga-on="click"
              :to="{ name: 'membership' }"
              :ga-event-category="ga.userPortalNav.category"
              :ga-event-action="ga.userPortalNav.actions.inline"
              :ga-event-label="ga.userPortalNav.labels.membership"
            >
              More about your membership
            </router-link>
          </span>
        </li>
        <li>
          <span class="c-link-list__arrow has-text-teal">
            <strong>&rarr;</strong>
          </span>
          <span class="has-text-gray-dark">
            <a
              ga-on="click"
              :href="donateUrl"
              :ga-event-category="ga.donations.category"
              :ga-event-action="ga.donations.actions['membership-intent']"
              :ga-event-label="ga.donations.labels['upgrade-membership']"
            >
              Become a sustaining member
            </a>
          </span>
        </li>
      </ul>
    </template>
  </summary-box>
</template>

<script>
import SummaryBox from '../../../components/SummaryBox.vue';

export default {
  name: 'OneTime',

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
