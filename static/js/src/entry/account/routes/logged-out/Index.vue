<template>
  <div>
    <no-routes-nav-bar />
    <main class="l-minimal has-bg-white-off has-xl-padding">
      <div class="l-minimal__content t-align-center">
        <h1 class="has-xl-btm-marg">You're logged out</h1>
        <p>Redirecting&hellip;</p>
      </div>
    </main>
    <no-routes-site-footer />
  </div>
</template>

<script>
import { clearLoggedInFlag } from '../../utils/storage';
import { redirect } from '../../utils/auth-actions';
import routeMixin from '../mixin';

export default {
  name: 'LoggedOutRoute',

  mixins: [routeMixin],

  data() {
    return { title: 'Logged Out' };
  },

  mounted() {
    clearLoggedInFlag();
    redirect(this.$route.query.next);
  },
};
</script>
