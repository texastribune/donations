<template>
  <summary-box heading="membership" :display="{ isExpired: true }">
    <template v-slot:content>
      <p class="has-text-gray-dark t-space-heading-m">
        Thanks for your previous support!
        <span class="has-text-error"
          >Your membership expired on
          <strong>{{ membershipExpirationDate | longDate }}</strong
          >.</span
        >
        <template v-if="lastTransaction.last4">
          Your last donation of
          <strong>{{ lastTransaction.amount | currency }}</strong> was charged
          on <strong>{{ lastTransaction.date | longDate }}</strong
          >, to your card ending in <strong>{{ lastTransaction.last4 }}</strong
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
    <template v-slot:links>
      <ul class="c-link-list">
        <li class="has-m-btm-marg">
          <span class="c-link-list__arrow has-text-teal">
            <strong>&rarr;</strong>
          </span>
          <span class="has-text-gray-dark">
            <a
              :href="isCircleDonor ? circleUrl : donateUrl"
              ga-on="click"
              :ga-event-category="ga.donations.category"
              :ga-event-action="ga.donations.actions['membership-intent']"
              :ga-event-label="ga.donations.labels['renew-membership']"
            >
              Renew your membership
            </a>
          </span>
        </li>
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
        <li>
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
      </ul>
    </template>
  </summary-box>
</template>

<script>
import SummaryBox from '../../../components/SummaryBox.vue';

export default {
  name: 'Expired',

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

    isCircleDonor: {
      type: Boolean,
      required: true,
    },
  },
};
</script>
