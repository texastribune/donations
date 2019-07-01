<template>
  <div>
    <nav-bar :show-route-links="false" />
    <main class="l-minimal has-bg-white-off has-xl-padding">
      <div class="l-minimal__content t-linkstyle--underlined">
        <h1 class="has-xl-btm-marg">Please verify your account</h1>
        <p class="t-space-heading-m">
          Thanks for creating a Texas Tribune account &mdash; you’re almost
          done! To view your account, we need you to verify your email address:
          <strong>{{ email }}</strong
          >. Check your inbox for an email from The Texas Tribune with the
          subject line &quot;Please confirm your account,&quot; then click to
          verify your email. Having trouble? Contact
          <a
            href="mailto:community@texastribune.org?subject=account%20technical%20error"
            >community@texastribune.org</a
          >.
        </p>
      </div>
    </main>
    <site-footer :show-route-links="false" />
  </div>
</template>

<script>
import tokenUser from './mixins/token-user';

export default {
  name: 'UnverifiedView',

  mixins: [tokenUser],

  computed: {
    email() {
      return this.tokenUser.email;
    },
  },

  mounted() {
    window.onpopstate = () => {
      window.location.reload();
    };
  },
};
</script>
