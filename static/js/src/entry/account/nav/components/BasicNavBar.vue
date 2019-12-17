<template>
  <token-user-nav-provider v-slot="slotProps">
    <nav-bar
      :show-edit-contact-info-link="false"
      :show-ambassador-link="false"
      :show-home-link="false"
      :show-blast-link="false"
      :show-membership-link="false"
      :is-logged-in="slotProps.isLoggedIn"
    />
  </token-user-nav-provider>
</template>

<script>
import TokenUserNavProvider from '../providers/TokenUserNavProvider.vue';
import NavBar from './NavBar.vue';

export default {
  name: 'BasicNavBar',

  components: { TokenUserNavProvider, NavBar },
};
</script>
