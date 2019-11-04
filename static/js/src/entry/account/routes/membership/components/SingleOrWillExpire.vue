<template>
  <section class="c-detail-box">
    <div class="has-xxl-btm-marg"><info-list :items="data" /></div>

    <ul class="c-link-list t-links-underlined">
      <li class="has-xs-btm-marg">
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
      <li v-if="isSingleDonor">
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
  </section>
</template>

<script>
import InfoList from '../../../components/InfoList.vue';

export default {
  name: 'MembershipSingleOrWillExpire',

  components: { InfoList },

  props: {
    data: {
      type: Array,
      required: true,
    },

    isSingleDonor: {
      type: Boolean,
      required: true,
    },
  },
};
</script>
