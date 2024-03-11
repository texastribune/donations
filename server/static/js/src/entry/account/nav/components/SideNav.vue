<template>
  <nav class="c-side-nav">
    <transition name="has-fade">
      <ul class="c-side-nav__outer t-size-s">
        <li class="has-xxs-btm-marg">
          <router-link
            exact
            class="has-text-black-off has-text-hover-gray"
            active-class="is-active"
            ga-on="click"
            :to="{ name: 'accountOverview' }"
            :ga-event-category="ga.userPortalNav.category"
            :ga-event-action="ga.userPortalNav.actions.side"
            :ga-event-label="ga.userPortalNav.labels.home"
          >
            Account Overview
          </router-link>
        </li>
        <li class="has-xxs-btm-marg">
          <router-link
            exact
            class="has-text-black-off has-text-hover-gray"
            active-class="is-active"
            :to="{ name: 'edit-contact-info' }"
            :ga-event-category="ga.userPortalNav.category"
            :ga-event-action="ga.userPortalNav.actions.side"
            :ga-event-label="ga.userPortalNav.labels['edit-contact-info']"
          >
            Profile Settings
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
        <li v-if="showBlastLink">
          <router-link
            class="has-text-black-off has-text-hover-gray"
            active-class="is-active"
            ga-on="click"
            :to="{ name: 'blast' }"
            :ga-event-category="ga.userPortalNav.category"
            :ga-event-action="ga.userPortalNav.actions.side"
            :ga-event-label="ga.userPortalNav.labels.blast"
          >
            The Blast
          </router-link>
        </li>
      </ul>
    </transition>
  </nav>
</template>

<script>
export default {
  name: 'SideNav',

  props: {
    showMembershipLink: {
      type: Boolean,
      required: true,
    },

    showPaymentsLink: {
      type: Boolean,
      required: true,
    },

    showBlastLink: {
      type: Boolean,
      required: true,
    },
  },
};
</script>
