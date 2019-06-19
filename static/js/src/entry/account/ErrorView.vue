<template>
  <div>
    <nav-bar :show-route-links="false" />
    <main class="l-minimal has-bg-white-off has-xl-padding">
      <div class="l-minimal__content t-linkstyle--underlined">
        <h1 class="has-xl-btm-marg">Sorry about that.</h1>
        <p class="has-s-btm-marg t-space-heading-m">
          An error occurred, and we're working hard to fix it.
        </p>
        <p class="t-space-heading-m">
          You can return to your <a href="/account">account overview</a> or
          email
          <a href="mailto:community@texastribune.org"
            >community@texastribune.org</a
          >
          if the issue persists.
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
