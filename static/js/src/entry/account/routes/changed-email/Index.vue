<template>
  <div>
    <no-routes-nav-bar />
    <main
      v-if="!routeIsFetching"
      class="l-minimal has-bg-white-off has-xl-padding"
    >
      <div class="l-minimal__content t-linkstyle--underlined">
        <h1 class="has-xl-btm-marg">Please verify your email address change</h1>
        <p class="t-space-heading-m has-b-btm-marg">
          Thanks for updating your email address! To log back into your account,
          we need you to verify your new email address:
          <strong>{{ newEmail }}</strong
          >.
        </p>
        <p class="t-space-heading-m">
          Check your inbox for an email from The Texas Tribune with the subject
          line "Please confirm your account," then click to verify your email.
          Having trouble? Contact
          <a
            href="mailto:community@texastribune.org?subject=account%20technical%20error"
            >community@texastribune.org</a
          >.
        </p>
      </div>
    </main>
    <no-routes-site-footer />
  </div>
</template>

<script>
import routeMixin from '../../mixins/route';

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
