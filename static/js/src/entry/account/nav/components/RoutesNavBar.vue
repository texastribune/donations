<template>
  <user-nav-container>
    <template v-slot="slotProps">
      <nav-bar
        :user-fetch-complete="slotProps.userFetchComplete"
        :show-home-link="slotProps.showHomeLink"
        :show-blast-link="slotProps.showBlastLinks"
        :show-membership-link="slotProps.showMembershipLink"
        :is-logged-in="slotProps.isLoggedIn"
      />
    </template>
  </user-nav-container>
</template>

<script>
import UserNavContainer from '../containers/UserNavContainer.vue';
import NavBar from './NavBar.vue';

export default {
  name: 'RoutesNavBar',

  components: { UserNavContainer, NavBar },
};
</script>
