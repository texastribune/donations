<template>
  <div>
    <div v-if="context.isFetching">Fetching data ...</div>
    <div v-if="isCheckingUser">Checking user ...</div>
    <div v-else>
      <button @click="logOut">Log out</button>
      <ul>
        <li><router-link :to="{ name: 'home' }">Home</router-link></li>
        <li>
          <router-link :to="{ name: 'membership' }">Membership</router-link>
        </li>
        <li><router-link :to="{ name: 'payments' }">Payments</router-link></li>
        <li><router-link :to="{ name: 'blast' }">Blast</router-link></li>
        <li>
          <router-link :to="{ name: 'blast-payments' }"
            >Blast Payments</router-link
          >
        </li>
      </ul>
      <router-view />
    </div>
  </div>
</template>

<script>
import { mapActions } from 'vuex';

import contextMixin from '../../mixins/context';
import userMixin from '../../mixins/user';
import { LoggedOutError, Auth0Error } from '../../errors';

export default {
  name: 'Index',

  mixins: [contextMixin, userMixin],

  data() {
    return { isCheckingUser: true, data: [] };
  },

  mounted() {
    this.getUserOrRedirect();
  },

  methods: {
    ...mapActions('user', ['getUser']),

    async getUserOrRedirect() {
      try {
        await this.getUser();
        this.isCheckingUser = false;
      } catch (err) {
        if (err instanceof LoggedOutError) {
          this.logIn();
        } else if (err instanceof Auth0Error) {
          this.isCheckingUser = false;
          this.context.setError(true);
        }
      }
    },
  },
};
</script>
