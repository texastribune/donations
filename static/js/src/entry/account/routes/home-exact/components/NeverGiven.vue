<template>
  <summary-box heading="become a member" :display="{ isExpired: false }">
    <template v-slot:content>
      <p class="has-text-gray-dark t-space-heading-m">
        Our nonprofit newsroom relies on the support of readers like you to keep
        our stories free and accessible for all. Are you ready to join our
        member community?
      </p>
    </template>
    <template v-slot:links>
      <ul class="c-link-list">
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
              :ga-event-label="ga.donations.labels['never-given']"
            >
              Learn more and join now
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
  name: 'NeverGiven',

  components: { SummaryBox },
};
</script>
