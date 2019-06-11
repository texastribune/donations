<template>
  <nav-bar :show-route-links="showRouteLinks" :user="user" />
</template>

<script>
import NavBar from '../components/NavBar.vue';
import userMixin from '../routes/home/mixins/user';

export default {
  name: 'NavBarContainer',

  components: { NavBar },

  mixins: [userMixin],

  props: {
    showRouteLinks: {
      type: Boolean,
      default: true,
    },
  },
};
</script>
