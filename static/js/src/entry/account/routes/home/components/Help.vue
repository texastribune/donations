<template>
  <aside
    class="c-help has-ump-side-padding has-ump-btm-padding has-white-off-bg-until-bp-l"
  >
    <h2 class="t-uppercase t-size-b has-s-btm-marg">Contact us</h2>
    <p class="t-linkstyle--underlined has-text-gray-dark">
      <template v-if="home || edit || ambassador">
        Have questions about your account? Or feedback about this website? Email
        <a
          href="mailto:community@texastribune.org"
          ga-on="click"
          :ga-event-category="ga.userPortal.category"
          :ga-event-action="ga.userPortal.actions['contact-us']"
          :ga-event-label="gaEventLabel"
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
          :ga-event-label="gaEventLabel"
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
          :ga-event-label="gaEventLabel"
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
    home: {
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

    edit: {
      type: Boolean,
      default: false,
    },

    ambassador: {
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

  computed: {
    // eslint-disable-next-line consistent-return, vue/return-in-computed-property
    gaEventLabel() {
      const {
        home,
        blast,
        blastPayments,
        edit,
        ambassador,
        membership,
        payments,
      } = this;

      if (home) return this.ga.userPortal.labels.home;
      if (blast) return this.ga.userPortal.labels.blast;
      if (blastPayments) return this.ga.userPortal.labels['blast-payments'];
      if (edit) return this.ga.userPortal.labels['edit-contact-info'];
      if (ambassador) return this.ga.userPortal.labels.ambassador;
      if (membership) return this.ga.userPortal.labels.membership;
      if (payments) return this.ga.userPortal.labels.payments;
    },
  },
};
</script>
