<template>
  <token-user-provider v-slot="{ accessToken }">
    <user-provider v-slot="{ isBlastSubscriber, hasGivenNotCustom }">
      <nav-bar
        show-user-links
        :show-blast-link="!routeIsFetching && isBlastSubscriber"
        :show-membership-link="!routeIsFetching && hasGivenNotCustom"
        :is-logged-in="!!accessToken"
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

  props: {
    routeIsFetching: {
      type: Boolean,
      required: true,
    },
  },
};
</script>
