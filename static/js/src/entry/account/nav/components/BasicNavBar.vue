<template>
  <token-user-provider v-slot="{ accessToken }">
    <nav-bar :show-user-links="false" :is-logged-in="!!accessToken" />
  </token-user-provider>
</template>

<script>
import TokenUserProvider from '../../store/token-user/Provider.vue';
import NavBar from './NavBar.vue';

export default {
  name: 'BasicNavBar',

  components: { NavBar },

  mixins: [TokenUserProvider],
};
</script>
