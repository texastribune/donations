<template>
  <div>
    <ul class="c-link-list t-links-underlined">
      <li
        v-if="isRecurringDonor || isSingleDonor || isCircleDonor"
        class="has-m-btm-marg"
      >
        <span class="c-link-list__arrow has-text-teal">
          <strong>&rarr;</strong>
        </span>
        <span class="has-text-gray-dark">
          <router-link
            ga-on="click"
            :ga-event-category="ga.userPortalNav.category"
            :ga-event-action="ga.userPortalNav.actions.inline"
            :ga-event-label="ga.userPortalNav.labels.membership"
            :to="{ name: 'membership' }"
          >
            See your membership status
          </router-link>
        </span>
      </li>
      <li v-if="isBlastSubscriber" class="has-m-btm-marg">
        <span class="c-link-list__arrow has-text-teal">
          <strong>&rarr;</strong>
        </span>
        <span class="has-text-gray-dark">
          <router-link
            ga-on="click"
            :ga-event-category="ga.userPortalNav.category"
            :ga-event-action="ga.userPortalNav.actions.inline"
            :ga-event-label="ga.userPortalNav.labels.blast"
            :to="{ name: 'blast' }"
          >
            See your subscription to The Blast
          </router-link>
        </span>
      </li>
      <li
        v-if="!pwResetSuccess && !pwResetFailure"
        :style="[
          isStaff && { 'pointer-events': 'none' },
          isStaff && { opacity: '.2' },
        ]"
      >
        <span class="c-link-list__arrow has-text-teal">
          <strong>&rarr;</strong>
        </span>
        <span class="has-text-gray-dark">
          <button class="c-link-button" @click="resetPassword">
            Reset your password
          </button>
        </span>
      </li>
    </ul>

    <p v-if="pwResetSuccess" class="t-size-xs has-text-gray">
      Check your inbox for an email from The Texas Tribune with the subject line
      &quot;Reset your password.&quot;
    </p>
    <p v-if="pwResetFailure" class="t-size-xs has-text-gray">
      There was an issue resetting your password. If you continue having
      trouble, email
      <a href="mailto:community@texastribune.org">community@texastribune.org </a
      >.
    </p>
  </div>
</template>

<script>
export default {
  name: 'EditContactInfoLinks',

  props: {
    pwResetSuccess: {
      type: Boolean,
      required: true,
    },

    pwResetFailure: {
      type: Boolean,
      required: true,
    },

    isStaff: {
      type: Boolean,
      required: true,
    },

    isBlastSubscriber: {
      type: Boolean,
      required: true,
    },

    isRecurringDonor: {
      type: Boolean,
      required: true,
    },

    isSingleDonor: {
      type: Boolean,
      required: true,
    },

    isCircleDonor: {
      type: Boolean,
      required: true,
    },
  },

  methods: {
    resetPassword() {
      this.$emit('resetPassword');

      window.dataLayer.push({
        event: this.ga.customEventName,
        gaCategory: this.ga.userPortal.category,
        gaAction: this.ga.userPortal.actions['reset-password'],
        gaLabel: this.ga.userPortal.labels['edit-contact-info'],
      });
    },
  },
};
</script>
