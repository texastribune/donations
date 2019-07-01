<template>
  <div>
    <nav-bar :show-route-links="false" />
    <main class="l-minimal has-bg-white-off has-xl-padding">
      <div class="l-minimal__content t-align-center">
        <h1 class="has-xl-btm-marg">You're logged in.</h1>
        <p class="t-space-heading-m">
          Redirecting back to your original location &hellip;
        </p>
      </div>
    </main>
    <site-footer :show-route-links="false" />
  </div>
</template>

<script>
import { setFlag, redirectAfterLogIn } from '../../utils/auth-actions';
import routeMixin from '../../mixins/route';

export default {
  name: 'LoggedInRoute',

  mixins: [routeMixin],

  computed: {
    route() {
      return {
        isExact: true,
        isProtected: false,
        title: 'Logged In',
      };
    },
  },

  mounted() {
    setFlag();
    redirectAfterLogIn();
  },

  methods: {
    async fetchData() {
      return true;
    },
  },
};
</script>
