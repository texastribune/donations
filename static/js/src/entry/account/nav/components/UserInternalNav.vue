<template>
  <reset-password-provider v-slot="{ pwResetSuccess, pwResetFailure, pwReset }">
    <user-provider
      v-slot="{
        isNeverGiven,
        isSingleDonor,
        isCircleDonor,
        hasGivenNotCustom,
        isExpired,
        isFormerBlastSubscriber,
        isBlastSubscriber,
      }"
    >
      <div>
        <ul
          :class="(pwResetSuccess || pwResetFailure) && 'has-m-btm-marg'"
          class="c-link-list t-links-underlined"
        >
          <slot name="items"></slot>

          <internal-nav-item v-if="isNeverGiven && showJoinNow">
            <a
              ga-on="click"
              :href="donateUrl"
              :ga-event-category="ga.donations.category"
              :ga-event-action="ga.donations.actions['membership-intent']"
              :ga-event-label="ga.donations.labels['never-given']"
            >
              Learn more and join now
            </a>
          </internal-nav-item>
          <internal-nav-item
            v-if="hasGivenNotCustom && isExpired && showRenewMembership"
          >
            <a
              ga-on="click"
              :href="isCircleDonor ? circleUrl : donateUrl"
              :ga-event-category="ga.donations.category"
              :ga-event-action="ga.donations.actions['membership-intent']"
              :ga-event-label="ga.donations.labels['renew-membership']"
            >
              Renew your membership
            </a>
          </internal-nav-item>
          <internal-nav-item v-if="isFormerBlastSubscriber && showRenewBlast">
            <a
              ga-on="click"
              href="/blastform"
              :ga-event-category="ga.blastIntent.category"
              :ga-event-action="ga.blastIntent.actions['renew-blast']"
              :ga-event-label="ga.blastIntent.labels['user-portal']"
            >
              Renew your subscription to The Blast
            </a>
          </internal-nav-item>
          <internal-nav-item
            v-if="isSingleDonor && !isExpired && showBecomeSustaining"
          >
            <a
              ga-on="click"
              :href="donateUrl"
              :ga-event-category="ga.donations.category"
              :ga-event-action="ga.donations.actions['membership-intent']"
              :ga-event-label="ga.donations.labels['upgrade-membership']"
            >
              Become a sustaining member
            </a>
          </internal-nav-item>
          <internal-nav-item
            v-if="showResetPw && !pwResetSuccess && !pwResetFailure"
          >
            <button class="c-link-button" @click="pwReset(pwResetGaLabel)">
              Reset your password
            </button>
          </internal-nav-item>
          <internal-nav-item v-if="!isNeverGiven && showDonationHistory">
            <router-link
              ga-on="click"
              :to="{ name: 'payments' }"
              :ga-event-category="ga.userPortalNav.category"
              :ga-event-action="ga.userPortalNav.actions.inline"
              :ga-event-label="ga.userPortalNav.labels.payments"
            >
              See your donation history
            </router-link>
          </internal-nav-item>
          <internal-nav-item v-if="hasGivenNotCustom && showMembershipStatus">
            <router-link
              ga-on="click"
              :to="{ name: 'membership' }"
              :ga-event-category="ga.userPortalNav.category"
              :ga-event-action="ga.userPortalNav.actions.inline"
              :ga-event-label="ga.userPortalNav.labels.membership"
            >
              <slot name="membership-text">See your membership status</slot>
            </router-link>
          </internal-nav-item>
          <internal-nav-item v-if="isBlastSubscriber && showBlastSubscription">
            <router-link
              ga-on="click"
              :to="{ name: 'blast' }"
              :ga-event-category="ga.userPortalNav.category"
              :ga-event-action="ga.userPortalNav.actions.inline"
              :ga-event-label="ga.userPortalNav.labels.blast"
            >
              <slot name="blast-text">See your subscription to The Blast</slot>
            </router-link>
          </internal-nav-item>
          <internal-nav-item v-if="isBlastSubscriber && showBlastPayments">
            <router-link
              ga-on="click"
              :to="{ name: 'blast-payments' }"
              :ga-event-category="ga.userPortalNav.category"
              :ga-event-action="ga.userPortalNav.actions.inline"
              :ga-event-label="ga.userPortalNav.labels['blast-payments']"
            >
              See your payment history
            </router-link>
          </internal-nav-item>
          <internal-nav-item v-if="showEditProfile">
            <router-link
              ga-on="click"
              :to="{ name: 'edit-contact-info' }"
              :ga-event-category="ga.userPortalNav.category"
              :ga-event-action="ga.userPortalNav.actions.inline"
              :ga-event-label="ga.userPortalNav.labels['edit-contact-info']"
            >
              Edit your profile
            </router-link>
          </internal-nav-item>
          <internal-nav-item v-if="showAmbassador">
            <router-link
              ga-on="click"
              :to="{ name: 'ambassador' }"
              :ga-event-category="ga.userPortalNav.category"
              :ga-event-action="ga.userPortalNav.actions.inline"
              :ga-event-label="ga.userPortalNav.labels.ambassador"
            >
              Become a Tribune Ambassador
            </router-link>
          </internal-nav-item>
        </ul>

        <p v-if="pwResetSuccess" class="t-size-xs has-text-gray">
          Check your inbox for an email from The Texas Tribune with the subject
          line &quot;Reset your password.&quot;
        </p>
        <p v-if="pwResetFailure" class="t-size-xs has-text-gray">
          There was an issue resetting your password. If you continue having
          trouble, email
          <a href="mailto:community@texastribune.org"
            >community@texastribune.org </a
          >.
        </p>
      </div>
    </user-provider>
  </reset-password-provider>
</template>

<script>
import UserProvider from '../../store/user/Provider.vue';
import ResetPasswordProvider from '../../providers/ResetPasswordProvider.vue';
import InternalNavItem from './InternalNavItem.vue';

export default {
  name: 'UserInternalNav',

  components: {
    UserProvider,
    ResetPasswordProvider,
    InternalNavItem,
  },

  props: {
    showDonationHistory: {
      type: Boolean,
      default: false,
    },

    showMembershipStatus: {
      type: Boolean,
      default: false,
    },

    showBlastSubscription: {
      type: Boolean,
      default: false,
    },

    showBlastPayments: {
      type: Boolean,
      default: false,
    },

    showEditProfile: {
      type: Boolean,
      default: false,
    },

    showAmbassador: {
      type: Boolean,
      default: false,
    },

    showBecomeSustaining: {
      type: Boolean,
      default: false,
    },

    showJoinNow: {
      type: Boolean,
      default: false,
    },

    showRenewMembership: {
      type: Boolean,
      default: false,
    },

    showRenewBlast: {
      type: Boolean,
      default: false,
    },

    showResetPw: {
      type: Boolean,
      default: false,
    },

    pwResetGaLabel: {
      type: String,
      default: '',
    },
  },
};
</script>
