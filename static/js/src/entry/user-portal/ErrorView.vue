<template>
  <div>
    <nav-bar :show-route-links="false" />
    <main class="l-minimal has-bg-white-off has-xl-padding">
      <div class="l-align-center-self l-align-center-x t-linkstyle--underlined">
        <h1 class="has-xl-btm-marg">Sorry about that.</h1>
        <p class="has-s-btm-marg">
          An error occurred, and we're working hard to fix it.
        </p>
        <p>
          You can return to your <a href="/user-portal">account overview</a> or
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
