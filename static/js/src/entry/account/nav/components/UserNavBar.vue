<template>
  <user-nav-provider v-slot="slotProps">
    <nav-bar
      show-home-link
      show-edit-contact-info-link
      show-ambassador-link
      :show-blast-link="!routeIsFetching && slotProps.showBlastLinks"
      :show-membership-link="!routeIsFetching && slotProps.showMembershipLink"
      :is-logged-in="slotProps.isLoggedIn"
    />
  </user-nav-provider>
</template>

<script>
import UserNavProvider from '../providers/UserNavProvider.vue';
import NavBar from './NavBar.vue';

export default {
  name: 'UserNavBar',

  components: { UserNavProvider, NavBar },

  props: {
    routeIsFetching: {
      type: Boolean,
      required: true,
    },
  },
};
</script>
