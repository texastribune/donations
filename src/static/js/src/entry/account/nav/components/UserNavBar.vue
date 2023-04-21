<template>
  <token-user-provider v-slot="{ tokenUser: { isLoggedIn } }">
    <user-provider v-slot="{ user: { isBlastSubscriber, hasGivenNotCustom } }">
      <nav-bar
        show-user-links
        :show-blast-link="isBlastSubscriber"
        :show-membership-link="hasGivenNotCustom"
        :is-logged-in="isLoggedIn"
      />
    </user-provider>
  </token-user-provider>
</template>

<script>
import TokenUserProvider from '../../store/token-user/Provider.vue';
import UserProvider from '../../store/user/Provider.vue';

import NavBar from './NavBar.vue';

export default {
  name: 'UserNavBar',

  components: { TokenUserProvider, UserProvider, NavBar },
};
</script>
