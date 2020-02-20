<template>
  <div>
    <basic-nav-bar />
    <main class="l-minimal has-bg-white-off has-xl-padding">
      <div class="l-minimal__content t-align-center">
        <h1 class="has-xl-btm-marg">You're logged out</h1>
        <p>Redirecting&hellip;</p>
      </div>
    </main>
    <basic-site-footer />
  </div>
</template>

<script>
import { redirect, clearLoggedInFlag } from '../../utils/auth-actions';
import routeMixin from '../mixin';

export default {
  name: 'LoggedOutRoute',

  mixins: [routeMixin],

  mounted() {
    clearLoggedInFlag();
    redirect(this.$route.query);
  },
};
</script>
