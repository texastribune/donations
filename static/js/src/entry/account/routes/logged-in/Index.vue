<template>
  <div>
    <no-routes-nav-bar />
    <main class="l-minimal has-bg-white-off has-xl-padding">
      <div class="l-minimal__content t-align-center">
        <h1 class="has-xl-btm-marg">You're logged in.</h1>
        <p class="t-space-heading-m">
          Redirecting to your account overview &hellip;
        </p>
      </div>
    </main>
    <no-routes-site-footer />
  </div>
</template>

<script>
import { redirectAfterLogIn } from '../../utils/auth-actions';
import { setLoggedInFlag } from '../../utils/storage';
import routeMixin from '../../mixins/route';

export default {
  name: 'LoggedInRoute',

  mixins: [routeMixin],

  data() {
    return { title: 'Logged In' };
  },

  mounted() {
    setLoggedInFlag();
    redirectAfterLogIn();
  },
};
</script>
