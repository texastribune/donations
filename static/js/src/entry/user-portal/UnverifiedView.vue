<template>
  <div>
    <nav-bar :show-route-links="false" />
    <main class="l-minimal has-bg-white-off has-xl-padding">
      <div class="l-minimal__content t-linkstyle--underlined">
        <h1 class="has-xl-btm-marg">Please verify your account</h1>
        <p class="t-space-heading-m">
          You're logged in, but we still need to verify your email address
          before you can view your Texas Tribune account. Check your inbox for
          an email from The Texas Tribune with the subject line &quot;Please
          confirm your account,&quot; then click to verify your email. Having
          trouble? Contact
          <a href="mailto:community@texastribune.org"
            >community@texastribune.org</a
          >.
        </p>
      </div>
    </main>
    <site-footer :show-route-links="false" />
  </div>
</template>

<script>
export default {
  name: 'UnverifiedView',

  mounted() {
    window.onpopstate = () => {
      window.location.reload();
    };
  },
};
</script>
