<template>
  <user-nav-container v-slot="slotProps">
    <nav-bar
      user-fetch-complete
      :show-edit-contact-info-link="false"
      :show-ambassador-link="false"
      :show-home-link="false"
      :show-blast-link="false"
      :show-membership-link="false"
      :is-logged-in="slotProps.isLoggedIn"
    />
  </user-nav-container>
</template>

<script>
import UserNavContainer from '../containers/UserNavContainer.vue';
import NavBar from './NavBar.vue';

export default {
  name: 'NoRoutesNavBar',

  components: { UserNavContainer, NavBar },
};
</script>
