<template>
  <token-user-provider v-slot="{ tokenUser: { isLoggedIn } }">
    <nav-bar :show-user-links="false" :is-logged-in="isLoggedIn" />
  </token-user-provider>
</template>

<script>
import TokenUserProvider from '../../store/token-user/Provider.vue';

import NavBar from './NavBar.vue';

export default {
  name: 'BasicNavBar',

  components: { NavBar, TokenUserProvider },

  mixins: [TokenUserProvider],
};
</script>
