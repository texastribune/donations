<template>
  <div>
    <basic-nav-bar />

    <main class="l-minimal has-bg-white-off has-xl-padding">
      <route-loader v-if="routeIsFetching" />

      <div v-else class="l-minimal__content">
        <logged-in
          :existing-email="existingEmail"
          :email-to-link="emailToLink"
          :ticket="ticket"
        />
        <logged-out
          :existing-email="existingEmail"
          :email-to-link="emailToLink"
          :ticket="ticket"
        />
      </div>
    </main>

    <basic-site-footer />
  </div>
</template>

<script>
import jwt from 'jsonwebtoken';

import routeMixin from '../mixin';
import tokenUserMixin from '../../store/token-user/mixin';
import userMixin from '../../store/user/mixin';
import RouteLoader from './components/RouteLoader.vue';
import LoggedOut from './components/LoggedOut.vue';
import LoggedIn from './containers/LoggedInContainer.vue';

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

    existingEmail() {
      const { existing_email: existingEmail } = jwt.decode(this.ticket);
      return existingEmail;
    },

    emailToLink() {
      const { email_to_link: emailToLink } = jwt.decode(this.ticket);
      return emailToLink;
    },
  },

  methods: {
    // eslint-disable-next-line consistent-return
    fetchData() {
      if (this.tokenUser.isLoggedIn) {
        return this.user.getUser();
      }
    },
  },
};
</script>
