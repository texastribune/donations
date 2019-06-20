<template>
  <div>
    <nav-bar :show-route-links="false" />
    <main class="l-minimal has-bg-white-off has-xl-padding">
      <div class="l-minimal__content t-linkstyle--underlined">
        <h1 class="has-xl-btm-marg">Sorry about that.</h1>
        <p class="has-s-btm-marg t-space-heading-m">
          We’re having trouble loading your account information, and we're
          working hard to fix it.
        </p>
        <p class="t-space-heading-m">
          Click here to return to your <a href="/account">account overview</a>.
          If the issue persists, contact us at
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
export default {
  name: 'ErrorView',

  mounted() {
    window.onpopstate = () => {
      window.location.reload();
    };
  },
};
</script>
