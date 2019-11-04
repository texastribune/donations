<template>
  <div>
    <no-routes-nav-bar />
    <main
      v-if="!routeIsFetching"
      class="l-minimal has-bg-white-off has-xl-padding"
    >
      <div class="l-minimal__content t-links-underlined">
        <h1 class="has-xl-btm-marg">Please verify your email address change</h1>
        <p class="has-b-btm-marg">
          Thanks for updating your email address! To log back into your account,
          we need you to verify your new email address:
          <strong>{{ newEmail }}</strong
          >.
        </p>
        <p>
          Check your inbox for an email from The Texas Tribune with the subject
          line "Please confirm your login email change," then click to verify
          your email. Having trouble? Contact
          <a
            href="mailto:community@texastribune.org?subject=account%20technical%20error"
            ga-on="click"
            :ga-event-category="ga.userPortal.category"
            :ga-event-action="ga.userPortal.actions['contact-us']"
            :ga-event-label="ga.userPortal.labels['changed-email']"
            >community@texastribune.org</a
          >.
        </p>
      </div>
    </main>
    <no-routes-site-footer />
  </div>
</template>

<script>
import routeMixin from '../mixin';

export default {
  name: 'ChangedEmailRoute',

  mixins: [routeMixin],

  data() {
    return { title: 'Verify your changed email' };
  },

  computed: {
    newEmail() {
      return this.$route.query.email;
    },
  },
};
</script>
