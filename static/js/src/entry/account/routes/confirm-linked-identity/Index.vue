<template>
  <div>
    <no-routes-nav-bar />
    <main class="l-minimal has-bg-white-off has-xl-padding">
      <route-loader v-if="routeIsFetching" />
      <div v-else class="l-minimal__content">
        <logged-in :ticket="ticket" @goHome="goHome" />
        <logged-out :ticket="ticket" />
      </div>
    </main>
    <no-routes-site-footer />
  </div>
</template>

<script>
import routeMixin from '../../mixins/route';
import tokenUserMixin from '../../store/token-user/mixin';
import userMixin from '../../store/user/mixin';
import RouteLoader from './components/RouteLoader.vue';
import LoggedIn from './containers/LoggedInContainer.vue';
import LoggedOut from './containers/LoggedOutContainer.vue';

export default {
  name: 'ConfirmLinkedIdentityRoute',

  components: { LoggedIn, LoggedOut, RouteLoader },

  mixins: [routeMixin, userMixin, tokenUserMixin],

  data() {
    return { title: 'Confirm linked email address' };
  },

  computed: {
    ticket() {
      return this.$route.query.ticket;
    },
  },

  methods: {
    goHome() {
      this.$router.push({ name: 'home' });
    },

    // eslint-disable-next-line consistent-return
    fetchData() {
      if (this.accessToken) return this.getUser();
    },
  },
};
</script>
