<template>
  <aside
    :class="display.hasTopPadding && 'c-help--has-top-padding'"
    class="c-help has-ump-side-padding has-ump-btm-padding has-white-off-bg-until-bp-l"
  >
    <h2 class="t-uppercase t-size-b has-s-btm-marg">Need help?</h2>
    <p class="t-space-heading-m t-linkstyle--underlined has-text-gray-dark">
      <template v-if="home">
        If you have questions about your Texas Tribune account or would like to
        give us feedback on this experience, please contact us at
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
          href="mailto:community@texastribune.org"
          ga-on="click"
          :ga-event-category="ga.userPortal.category"
          :ga-event-action="ga.userPortal.actions['contact-us']"
          :ga-event-label="
            membership
              ? ga.userPortal.labels.membership
              : ga.userPortal.labels.payments
          "
        >
          community@texastribune.org </a
        >.
      </template>
      <template v-else-if="blast || blastPayments">
        To update your subscription to The Blast, contact us at
        <a
          href="mailto:community@texastribune.org"
          ga-on="click"
          :ga-event-category="ga.userPortal.category"
          :ga-event-action="ga.userPortal.actions['contact-us']"
          :ga-event-label="
            blast
              ? ga.userPortal.labels.blast
              : ga.userPortal.labels['blast-payments']
          "
        >
          community@texastribune.org </a
        >.
      </template>
    </p>
  </aside>
</template>

<script>
export default {
  name: 'Help',

  props: {
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
  },
};
</script>
