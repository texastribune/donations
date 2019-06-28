<template>
  <footer class="c-site-footer has-bg-black-off">
    <div class="c-site-footer__inner l-container--xl l-align-center-x">
      <div class="c-site-footer__col">
        <div class="has-b-btm-marg">
          <icon name="bug" :display="{ color: 'yellow', inlineSize: '4rem' }" />
        </div>

        <div
          class="has-notch has-notch--thin has-bg-yellow has-b-btm-marg"
          aria-hidden="true"
        />

        <p class="t-size-s has-text-white">
          &copy; {{ thisYear }} The Texas Tribune
        </p>
      </div>

      <div class="c-site-footer__col t-size-s">
        <h4
          class="c-site-footer__header has-text-yellow t-uppercase has-xs-btm-marg"
        >
          Your account
        </h4>
        <ul class="c-site-footer__links has-text-white">
          <li v-if="showRouteLinks">
            <router-link
              ga-on="click"
              :ga-event-category="ga.userPortalNav.category"
              :ga-event-action="ga.userPortalNav.actions.footer"
              :ga-event-label="ga.userPortalNav.labels.home"
              :to="{ name: 'home' }"
            >
              Account Overview
            </router-link>
          </li>
          <li v-if="showMembershipLink">
            <router-link
              ga-on="click"
              :ga-event-category="ga.userPortalNav.category"
              :ga-event-action="ga.userPortalNav.actions.footer"
              :ga-event-label="ga.userPortalNav.labels.membership"
              :to="{ name: 'membership' }"
            >
              Membership Status
            </router-link>
          </li>
          <li v-if="showPaymentsLink">
            <router-link
              ga-on="click"
              :ga-event-category="ga.userPortalNav.category"
              :ga-event-action="ga.userPortalNav.actions.footer"
              :ga-event-label="ga.userPortalNav.labels.payments"
              :to="{ name: 'payments' }"
            >
              Donation History
            </router-link>
          </li>
          <li v-if="showBlastLinks">
            <router-link
              ga-on="click"
              :ga-event-category="ga.userPortalNav.category"
              :ga-event-action="ga.userPortalNav.actions.footer"
              :ga-event-label="ga.userPortalNav.labels.blast"
              :to="{ name: 'blast' }"
            >
              The Blast Newsletter
            </router-link>
          </li>
          <li v-if="showBlastLinks">
            <router-link
              ga-on="click"
              :ga-event-category="ga.userPortalNav.category"
              :ga-event-action="ga.userPortalNav.actions.footer"
              :ga-event-label="ga.userPortalNav.labels['blast-payments']"
              :to="{ name: 'blast-payments' }"
            >
              The Blast Payment History
            </router-link>
          </li>
        </ul>
      </div>

      <div class="c-site-footer__col t-size-s">
        <h4
          class="c-site-footer__header has-text-yellow t-uppercase has-xs-btm-marg"
        >
          Info
        </h4>
        <ul class="c-site-footer__links has-text-white">
          <li>
            <a
              ga-on="click"
              :ga-event-category="ga.userPortalNav.category"
              :ga-event-action="ga.userPortalNav.actions.footer"
              :ga-event-label="ga.userPortalNav.labels['community-guidelines']"
              href="https://www.texastribune.org/about/community-guidelines/"
            >
              Community Guidelines
            </a>
          </li>
          <li>
            <a
              ga-on="click"
              :ga-event-category="ga.userPortalNav.category"
              :ga-event-action="ga.userPortalNav.actions.footer"
              :ga-event-label="ga.userPortalNav.labels['support-landing']"
              href="/donate"
            >
              About Membership
            </a>
          </li>
          <li>
            <a
              ga-on="click"
              :ga-event-category="ga.userPortalNav.category"
              :ga-event-action="ga.userPortalNav.actions.footer"
              :ga-event-label="ga.userPortalNav.labels['privacy-policy']"
              href="https://www.texastribune.org/about/privacy-policy/"
            >
              Privacy Policy
            </a>
          </li>
          <li>
            <a
              ga-on="click"
              :ga-event-category="ga.userPortalNav.category"
              :ga-event-action="ga.userPortalNav.actions.footer"
              :ga-event-label="ga.userPortalNav.labels['texas-tribune-home']"
              href="https://www.texastribune.org/"
            >
              texastribune.org
            </a>
          </li>
        </ul>
      </div>
    </div>
  </footer>
</template>

<script>
import getYear from 'date-fns/get_year';

export default {
  name: 'SiteFooter',

  props: {
    showRouteLinks: {
      type: Boolean,
      required: true,
    },

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

  computed: {
    thisYear() {
      return getYear(new Date());
    },
  },
};
</script>
