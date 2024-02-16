<template>
  <user-provider
    v-slot="{
      user: {
        isNeverGiven,
        isSingleDonor,
        isCircleDonor,
        hasGivenNotCustom,
        isExpired,
        isFormerBlastSubscriber,
        isBlastSubscriber,
      },
    }"
  >
    <div>
      <link-list>
        <slot name="items"></slot>

        <link-list-item v-if="isNeverGiven && showJoinNow">
          <template #main>
            <a
              ga-on="click"
              :href="urls.donate"
              :ga-event-category="ga.donations.category"
              :ga-event-action="ga.donations.actions['membership-intent']"
              :ga-event-label="ga.donations.labels['never-given']"
            >
              Learn more and join now
            </a>
          </template>
        </link-list-item>
        <link-list-item
          v-if="hasGivenNotCustom && isExpired && showRenewMembership"
        >
          <template #main>
            <a
              ga-on="click"
              :href="isCircleDonor ? urls.circle : urls.donate"
              :ga-event-category="ga.donations.category"
              :ga-event-action="ga.donations.actions['membership-intent']"
              :ga-event-label="ga.donations.labels['renew-membership']"
            >
              Renew your membership
            </a>
          </template>
        </link-list-item>
        <link-list-item v-if="isFormerBlastSubscriber && showRenewBlast">
          <template #main>
            <a
              ga-on="click"
              href="/blastform"
              :ga-event-category="ga.blastIntent.category"
              :ga-event-action="ga.blastIntent.actions['renew-blast']"
              :ga-event-label="ga.blastIntent.labels['user-portal']"
            >
              Renew your subscription to The Blast
            </a>
          </template>
        </link-list-item>
        <link-list-item
          v-if="isSingleDonor && !isExpired && showBecomeSustaining"
        >
          <template #main>
            <a
              ga-on="click"
              :href="urls.donate"
              :ga-event-category="ga.donations.category"
              :ga-event-action="ga.donations.actions['membership-intent']"
              :ga-event-label="ga.donations.labels['upgrade-membership']"
            >
              Become a sustaining member
            </a>
          </template>
        </link-list-item>

        <reset-password v-if="showResetPw" :ga-label="pwResetGaLabel" />

        <link-list-item v-if="!isNeverGiven && showDonationHistory">
          <template #main>
            <router-link
              ga-on="click"
              :to="{ name: 'payments' }"
              :ga-event-category="ga.userPortalNav.category"
              :ga-event-action="ga.userPortalNav.actions.inline"
              :ga-event-label="ga.userPortalNav.labels.payments"
            >
              See your donation history
            </router-link>
          </template>
        </link-list-item>
        <link-list-item v-if="!isNeverGiven && showUpdateCard">
          <template #main>
            <router-link
              ga-on="click"
              :to="{ name: 'membership' }"
              :ga-event-category="ga.userPortalNav.category"
              :ga-event-action="ga.userPortalNav.actions.inline"
              :ga-event-label="ga.userPortalNav.labels.membership"
            >
              Update your payment information
            </router-link>
          </template>
        </link-list-item>
        <link-list-item v-if="hasGivenNotCustom && showMembershipStatus">
          <template #main>
            <router-link
              ga-on="click"
              :to="{ name: 'membership' }"
              :ga-event-category="ga.userPortalNav.category"
              :ga-event-action="ga.userPortalNav.actions.inline"
              :ga-event-label="ga.userPortalNav.labels.membership"
            >
              <slot name="membership-text">See your membership status</slot>
            </router-link>
          </template>
        </link-list-item>
        <link-list-item v-if="isBlastSubscriber && showBlastSubscription">
          <template #main>
            <router-link
              ga-on="click"
              :to="{ name: 'blast' }"
              :ga-event-category="ga.userPortalNav.category"
              :ga-event-action="ga.userPortalNav.actions.inline"
              :ga-event-label="ga.userPortalNav.labels.blast"
            >
              <slot name="blast-text">See your subscription to The Blast</slot>
            </router-link>
          </template>
        </link-list-item>
        <link-list-item v-if="isBlastSubscriber && showBlastPayments">
          <template #main>
            <router-link
              ga-on="click"
              :to="{ name: 'blast-payments' }"
              :ga-event-category="ga.userPortalNav.category"
              :ga-event-action="ga.userPortalNav.actions.inline"
              :ga-event-label="ga.userPortalNav.labels['blast-payments']"
            >
              See your payment history
            </router-link>
          </template>
        </link-list-item>
        <link-list-item v-if="showEditProfile">
          <template #main>
            <router-link
              ga-on="click"
              :to="{ name: 'edit-contact-info' }"
              :ga-event-category="ga.userPortalNav.category"
              :ga-event-action="ga.userPortalNav.actions.inline"
              :ga-event-label="ga.userPortalNav.labels['edit-contact-info']"
            >
              Edit your profile
            </router-link>
          </template>
        </link-list-item>
      </link-list>
    </div>
  </user-provider>
</template>

<script>
import UserProvider from '../../store/user/Provider.vue';

import ResetPassword from '../../reset-password/components/LinkListItem.vue';
import LinkList from '../../components/LinkList.vue';
import LinkListItem from '../../components/LinkListItem.vue';

export default {
  name: 'UserInternalNav',

  components: {
    UserProvider,
    LinkList,
    LinkListItem,
    ResetPassword,
  },

  props: {
    showDonationHistory: {
      type: Boolean,
      default: false,
    },

    showUpdateCard: {
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
