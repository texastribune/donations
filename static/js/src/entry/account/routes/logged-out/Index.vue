<template>
  <div>
    <nav-bar :show-route-links="false" />
    <main class="l-minimal has-bg-white-off has-xl-padding">
      <div class="l-minimal__content t-align-center">
        <h1 class="has-xl-btm-marg">You're logged out.</h1>
        <p class="t-space-heading-m">
          Redirecting you to texastribune.org &hellip;
        </p>
      </div>
    </main>
    <site-footer :show-route-links="false" />
  </div>
</template>

<script>
import { clearFlag, redirectAfterLogOut } from '../../utils/auth-actions';
import routeMixin from '../../mixins/route';

export default {
  name: 'LoggedOutRoute',

  mixins: [routeMixin],

  computed: {
    route() {
      return {
        isExact: true,
        meetsCriteria: true,
        title: 'Logged Out',
      };
    },
  },

  mounted() {
    clearFlag();
    redirectAfterLogOut();
  },

  methods: {
    async fetchData() {
      return true;
    },
  },
};
</script>
