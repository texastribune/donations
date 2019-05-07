<template>
  <section>
    <h2>Need help?</h2>
    <p v-if="withFeedback">
      If you have questions about your Texas Tribune account or would like to
      give us feedback on this experience, please contact us at
      <a href="mailto:community@texastribune.org">community@texastribune.org</a
      >.
    </p>
    <p v-else>
      To update your membership status, contact us at
      <a href="mailto:community@texastribune.org">community@texastribune.org</a
      >.
    </p>
  </section>
</template>

<script>
export default {
  name: 'Help',

  props: {
    withFeedback: {
      type: Boolean,
      default: false,
    },
  },
};
</script>
