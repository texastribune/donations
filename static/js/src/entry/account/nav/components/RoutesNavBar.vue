<template>
  <user-nav-container v-slot="slotProps">
    <nav-bar
      show-home-link
      show-edit-contact-info-link
      show-ambassador-link
      :user-fetch-complete="slotProps.userFetchComplete"
      :show-blast-link="slotProps.showBlastLinks"
      :show-membership-link="slotProps.showMembershipLink"
      :is-logged-in="slotProps.isLoggedIn"
    />
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
