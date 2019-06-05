<template>
  <nav-bar :show-route-links="showRouteLinks" />
</template>

<script>
import NavBar from '../components/NavBar.vue';

export default {
  name: 'NavBarContainer',

  components: { NavBar },

  props: {
    showRouteLinks: {
      type: Boolean,
      default: true,
    },
  },
};
</script>
