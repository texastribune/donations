<template>
  <div>
    <basic-nav-bar />
    <main class="l-minimal has-bg-white-off has-xl-padding">
      <div class="l-minimal__content t-align-center">
        <h1 class="has-xl-btm-marg">You're logged in</h1>
        <p class="t-size-m">Redirecting&hellip;</p>
      </div>
    </main>
    <basic-site-footer />
  </div>
</template>

<script>
import routeMixin from '../mixin';

export default {
  name: 'LoggedInRoute',

  mixins: [routeMixin],

  mounted() {
    this.redirectFromQueryParams();
  },
};
</script>
