<template>
  <div>
    <no-routes-nav-bar />
    <main class="l-minimal has-bg-white-off has-xl-padding">
      <div class="l-minimal__content t-linkstyle--underlined">
        <h1 class="has-xl-btm-marg">Sorry about that.</h1>
        <p class="has-s-btm-marg">
          We’re having trouble loading your account information, and we're
          working hard to fix it.
        </p>
        <p>
          Click here to return to your <a href="/account">account overview</a>.
          If the issue persists, contact us at
          <a
            href="mailto:community@texastribune.org?subject=account%20technical%20error"
            ga-on="click"
            :ga-event-category="ga.userPortal.category"
            :ga-event-action="ga.userPortal.actions['contact-us']"
            :ga-event-label="ga.userPortal.labels.error"
            >community@texastribune.org</a
          >.
        </p>
      </div>
    </main>
    <no-routes-site-footer />
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
