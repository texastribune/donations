<template>
  <aside
    class="c-help has-ump-side-padding has-ump-btm-padding has-white-off-bg-until-bp-l"
  >
    <h2 class="t-uppercase t-size-b has-s-btm-marg">Contact us</h2>
    <p class="t-links-underlined has-text-gray-dark">
      <slot name="text"></slot>
      <a
        :href="`mailto:${computedEmail}?subject=${subject}`"
        ga-on="click"
        :ga-event-category="gaCategory"
        :ga-event-action="gaAction"
        :ga-event-label="computedGaLabel"
      >
        {{ computedEmail }} </a
      >.
    </p>
  </aside>
</template>

<script>
export default {
  name: 'ContactUs',

  props: {
    email: {
      type: String,
      default: '',
    },

    subject: {
      type: String,
      default: '',
    },

    gaLabel: {
      type: String,
      default: '',
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
  },
};
</script>
