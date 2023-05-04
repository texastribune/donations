<template>
  <p
    class="t-links-underlined has-text-gray-dark"
    :class="`t-size-${mergedDisplay.size} has-text-${mergedDisplay.color}`"
  >
    <slot name="text"></slot>
    <a
      :href="`mailto:${computedEmail}?subject=${computedSubject}`"
      ga-on="click"
      :ga-event-category="gaCategory"
      :ga-event-action="gaAction"
      :ga-event-label="computedGaLabel"
    >
      {{ computedEmail }} </a
    >.
  </p>
</template>

<script>
export default {
  name: 'ContactUsSmall',

  props: {
    gaLabel: {
      type: String,
      default: '',
    },

    email: {
      type: String,
      default: '',
    },

    subject: {
      type: String,
      default: '',
    },

    display: {
      type: Object,
      default: () => ({}),
    },

    isMembership: {
      type: Boolean,
      default: false,
    },

    isBlast: {
      type: Boolean,
      default: false,
    },
  },

  computed: {
    mergedDisplay() {
      return {
        size: 'b',
        color: 'gray-dark',
        ...this.display,
      };
    },

    gaCategory() {
      if (this.isMembership) {
        return this.ga.donations.category;
      }
      return this.ga.userPortal.category;
    },

    gaAction() {
      if (this.isMembership) {
        return this.ga.donations.actions['membership-intent'];
      }
      return this.ga.userPortal.actions['contact-us'];
    },

    computedGaLabel() {
      if (this.isMembership) {
        return this.ga.donations.labels['upgrade-contact'];
      }
      return this.gaLabel;
    },

    computedEmail() {
      const { email, isBlast, isMembership } = this;

      if (email) {
        return email;
      }
      if (isBlast) {
        return 'blast@texastribune.org';
      }
      if (isMembership) {
        return 'membership@texastribune.org';
      }

      return 'community@texastribune.org';
    },

    computedSubject() {
      const { subject, isBlast, isMembership } = this;

      if (subject) {
        return subject;
      }
      if (!isBlast && !isMembership) {
        return 'account%20technical%20error';
      }
      return '';
    },
  },
};
</script>
