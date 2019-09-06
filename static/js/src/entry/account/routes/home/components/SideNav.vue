<template>
  <nav class="c-side-nav">
    <transition name="has-fade">
      <ul v-if="userFetchComplete" class="c-side-nav__outer t-size-s">
        <li v-if="showHomeLink" class="has-xxs-btm-marg">
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
        <li v-if="showEditContactInfoLink" class="has-xxs-btm-marg">
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
        <li v-if="showAmbassadorLink" class="has-xxs-btm-marg">
          <router-link
            exact
            class="has-text-black-off has-text-hover-gray"
            active-class="is-active"
            :to="{ name: 'ambassador' }"
            :ga-event-category="ga.userPortalNav.category"
            :ga-event-action="ga.userPortalNav.actions.side"
            :ga-event-label="ga.userPortalNav.labels.ambassador"
          >
            Tribune Ambassadors
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
    showHomeLink: {
      type: Boolean,
      required: true,
    },

    showEditContactInfoLink: {
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

    showAmbassadorLink: {
      type: Boolean,
      required: true,
    },

    showBlastLink: {
      type: Boolean,
      required: true,
    },

    userFetchComplete: {
      type: Boolean,
      required: true,
    },
  },
};
</script>
