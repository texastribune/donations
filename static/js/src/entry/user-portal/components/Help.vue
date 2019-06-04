<template>
  <aside
    class="has-ump-side-padding has-ump-btm-padding has-white-off-bg-until-bp-l"
  >
    <h2 class="t-uppercase t-size-b has-s-btm-marg">Need help?</h2>
    <p class="t-space-heading-m t-linkstyle--underlined has-text-gray-dark">
      <template v-if="home">
        If you have questions about your Texas Tribune account or would like to
        give us feedback on this experience, please contact us at
        <a href="mailto:community@texastribune.org"
          >community@texastribune.org</a
        >.
      </template>
      <template v-else-if="membership">
        To update your membership status, contact us at
        <a href="mailto:community@texastribune.org"
          >community@texastribune.org</a
        >.
      </template>
      <template v-else-if="blast">
        To update your subscription to The Blast, contact us at
        <a href="mailto:community@texastribune.org"
          >community@texastribune.org</a
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

    blast: {
      type: Boolean,
      default: false,
    },
  },
};
</script>
