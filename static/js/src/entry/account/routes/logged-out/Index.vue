<template>
  <div>
    <no-routes-nav-bar />
    <main class="l-minimal has-bg-white-off has-xl-padding">
      <div class="l-minimal__content t-align-center">
        <h1 class="has-xl-btm-marg">You're logged out.</h1>
        <p class="t-space-heading-m">Redirecting you &hellip;</p>
      </div>
    </main>
    <no-routes-site-footer />
  </div>
</template>

<script>
import { redirectAfterLogOut } from '../../utils/auth-actions';
import { clearLoggedInFlag } from '../../utils/storage';
import routeMixin from '../../mixins/route';

export default {
  name: 'LoggedOutRoute',

  mixins: [routeMixin],

  data() {
    return { title: 'Logged Out' };
  },

  mounted() {
    clearLoggedInFlag();
    redirectAfterLogOut();
  },
};
</script>
