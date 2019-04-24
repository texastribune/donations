<template>
  <div v-if="isFetching">Loading...</div>
  <div v-else>
    <p>This is home.</p>
    <button @click="logOut">Log out</button>
    <ul>
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
</template>

<script>
import { mapActions } from 'vuex';
import axios from 'axios';

import contextMixin from '../../mixins/context';
import userMixin from '../../mixins/user';
import { LoggedOutError, Auth0Error } from '../../errors';

export default {
  name: 'Index',

  mixins: [contextMixin, userMixin],

  data() {
    return {
      isFetching: true,
    };
  },

  mounted() {
    this.getUserOrRedirect();
  },

  methods: {
    ...mapActions('user', ['getUser']),

    async getUserOrRedirect() {
      try {
        await this.getUser();
        this.isFetching = false;

        // eslint-disable-next-line
        const data = await axios.get(
          'https://www.texastribune.org/api/v2/content/'
        );
      } catch (err) {
        if (err instanceof LoggedOutError) {
          this.logIn();
        } else if (err instanceof Auth0Error) {
          this.setError(true);
          this.isFetching = false;
        }
      }
    },
  },
};
</script>
