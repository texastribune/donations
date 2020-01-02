<template>
  <nav-bar :show-user-links="false" :is-logged-in="isLoggedIn" />
</template>

<script>
import NavBar from './NavBar.vue';

export default {
  name: 'BasicNavBar',

  components: { NavBar },

  props: {
    isLoggedIn: {
      type: Boolean,
      required: true,
    },
  },
};
</script>
