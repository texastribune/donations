<template>
  <summary-box heading="membership" :display="{ isExpired: false }">
    <template v-slot:content>
      <p class="has-text-gray-dark t-space-heading-m">
        Thank you for being a Texas Tribune member!
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
              :to="{ name: 'payments' }"
              :ga-event-category="ga.userPortalNav.category"
              :ga-event-action="ga.userPortalNav.actions.inline"
              :ga-event-label="ga.userPortalNav.labels.payments"
            >
              See your donation history
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
  name: 'MDev',

  components: { SummaryBox },
};
</script>
