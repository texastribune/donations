<template>
  <summary-box heading="membership" :display="{ isExpired: false }">
    <template v-slot:content>
      <p
        v-if="nextTransaction.last4"
        class="has-text-gray-dark t-space-heading-m"
      >
        Thank you for being a Texas Tribune member! Your next
        <strong>{{ nextTransaction.period }}</strong> donation of
        <strong>{{ nextTransaction.amount | currency }}</strong> will be charged
        on <strong>{{ nextTransaction.date | longDate }}</strong
        >, to your card ending in <strong>{{ nextTransaction.last4 }}</strong
        >.
      </p>
      <p v-else class="has-text-gray-dark t-space-heading-m">
        Thank you for being a Texas Tribune member! Your next
        {{ nextTransaction.period }} donation of
        <strong>{{ nextTransaction.amount | currency }}</strong> is due on
        <strong>{{ nextTransaction.date | longDate }}</strong
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
    <template v-slot:bottom>
      <p class="has-text-gray-dark t-space-heading-m t-linkstyle--underlined">
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
  name: 'Circle',

  components: { SummaryBox },

  props: {
    nextTransaction: {
      type: Object,
      required: true,
    },
  },
};
</script>
