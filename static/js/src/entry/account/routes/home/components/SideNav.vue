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
          <strong>Account Overview</strong>
        </router-link>
      </li>
      <li v-if="showMembershipLinks" class="has-xxs-btm-marg">
        <router-link
          class="has-text-black-off has-text-hover-gray"
          active-class="is-active"
          ga-on="click"
          :to="{ name: 'membership' }"
          :ga-event-category="ga.userPortalNav.category"
          :ga-event-action="ga.userPortalNav.actions.side"
          :ga-event-label="ga.userPortalNav.labels.membership"
        >
          <strong>Membership</strong>
        </router-link>
        <ul class="c-side-nav__inner">
          <li>
            <router-link
              class="has-text-gray-dark has-text-hover-gray"
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
        </ul>
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
          <strong>The Blast Newsletter</strong>
        </router-link>
        <ul class="c-side-nav__inner">
          <li class="c-side-nav__item c-side-nav__item--inside">
            <router-link
              class="has-text-gray-dark has-text-hover-gray"
              active-class="is-active"
              ga-on="click"
              :to="{ name: 'blast-payments' }"
              :ga-event-category="ga.userPortalNav.category"
              :ga-event-action="ga.userPortalNav.actions.side"
              :ga-event-label="ga.userPortalNav.labels['blast-payments']"
            >
              Payment History
            </router-link>
          </li>
        </ul>
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

    showMembershipLinks: {
      type: Boolean,
      required: true,
    },
  },
};
</script>
