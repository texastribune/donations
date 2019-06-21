<template>
  <aside
    :class="display.hasTopPadding && 'c-help--has-top-padding'"
    class="c-help has-ump-side-padding has-ump-btm-padding has-white-off-bg-until-bp-l"
  >
    <h2 class="t-uppercase t-size-b has-s-btm-marg">Contact us</h2>
    <p class="t-space-heading-m t-linkstyle--underlined has-text-gray-dark">
      <template v-if="home">
        Have questions about your account? Or feedback about this website? Email
        <a
          href="mailto:community@texastribune.org"
          ga-on="click"
          :ga-event-category="ga.userPortal.category"
          :ga-event-action="ga.userPortal.actions['contact-us']"
          :ga-event-label="ga.userPortal.labels.home"
        >
          community@texastribune.org </a
        >.
      </template>
      <template v-else-if="membership || payments">
        To update your membership status, contact us at
        <a
          href="mailto:membership@texastribune.org"
          ga-on="click"
          :ga-event-category="ga.userPortal.category"
          :ga-event-action="ga.userPortal.actions['contact-us']"
          :ga-event-label="
            membership
              ? ga.userPortal.labels.membership
              : ga.userPortal.labels.payments
          "
        >
          membership@texastribune.org </a
        >.
      </template>
      <template v-else-if="blast || blastPayments">
        To update your subscription to The Blast, contact us at
        <a
          href="mailto:blast@texastribune.org"
          ga-on="click"
          :ga-event-category="ga.userPortal.category"
          :ga-event-action="ga.userPortal.actions['contact-us']"
          :ga-event-label="
            blast
              ? ga.userPortal.labels.blast
              : ga.userPortal.labels['blast-payments']
          "
        >
          blast@texastribune.org </a
        >.
      </template>
    </p>
  </aside>
</template>

<script>
export default {
  name: 'Help',

  props: {
    blast: {
      type: Boolean,
      default: false,
    },

    blastPayments: {
      type: Boolean,
      default: false,
    },

    display: {
      type: Object,
      default: () => ({ hasTopPadding: false }),
    },

    home: {
      type: Boolean,
      default: false,
    },

    membership: {
      type: Boolean,
      default: false,
    },

    payments: {
      type: Boolean,
      default: false,
    },
  },
};
</script>
