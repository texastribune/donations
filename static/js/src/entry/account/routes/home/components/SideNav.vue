<template>
  <nav class="c-side-nav">
    <ul class="c-side-nav__outer t-size-s">
      <li class="has-xxs-btm-marg">
        <router-link
          exact
          class="has-text-black-off has-text-hover-gray"
          active-class="is-active"
          ga-on="click"
          :to="{ name: 'home' }"
          :ga-event-category="ga.userPortalNav.category"
          :ga-event-action="ga.userPortalNav.actions.side"
          :ga-event-label="ga.userPortalNav.labels.home"
        >
          Account Overview
        </router-link>
      </li>
      <li v-if="showMembershipLink" class="has-xxs-btm-marg">
        <router-link
          class="has-text-black-off has-text-hover-gray"
          active-class="is-active"
          ga-on="click"
          :to="{ name: 'membership' }"
          :ga-event-category="ga.userPortalNav.category"
          :ga-event-action="ga.userPortalNav.actions.side"
          :ga-event-label="ga.userPortalNav.labels.membership"
        >
          Membership
        </router-link>
      </li>
      <li v-if="showPaymentsLink" class="has-xxs-btm-marg">
        <router-link
          class="has-text-black-off has-text-hover-gray"
          active-class="is-active"
          ga-on="click"
          :to="{ name: 'payments' }"
          :ga-event-category="ga.userPortalNav.category"
          :ga-event-action="ga.userPortalNav.actions.side"
          :ga-event-label="ga.userPortalNav.labels.payments"
        >
          Donation History
        </router-link>
      </li>
      <li v-if="showBlastLinks" class="has-xxs-btm-marg">
        <router-link
          class="has-text-black-off has-text-hover-gray"
          active-class="is-active"
          ga-on="click"
          :to="{ name: 'blast' }"
          :ga-event-category="ga.userPortalNav.category"
          :ga-event-action="ga.userPortalNav.actions.side"
          :ga-event-label="ga.userPortalNav.labels.blast"
        >
          The Blast Newsletter
        </router-link>
      </li>
      <li v-if="showBlastLinks">
        <router-link
          class="has-text-black-off has-text-hover-gray"
          active-class="is-active"
          ga-on="click"
          :to="{ name: 'blast-payments' }"
          :ga-event-category="ga.userPortalNav.category"
          :ga-event-action="ga.userPortalNav.actions.side"
          :ga-event-label="ga.userPortalNav.labels['blast-payments']"
        >
          The Blast Payment History
        </router-link>
      </li>
    </ul>
  </nav>
</template>

<script>
export default {
  name: 'SideNav',

  props: {
    showBlastLinks: {
      type: Boolean,
      required: true,
    },

    showMembershipLink: {
      type: Boolean,
      required: true,
    },

    showPaymentsLink: {
      type: Boolean,
      required: true,
    },
  },
};
</script>
