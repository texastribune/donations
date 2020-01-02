<template>
  <basic-nav-bar :is-logged-in="isLoggedIn" />
</template>

<script>
import tokenUserMixin from '../../store/token-user/mixin';
import BasicNavBar from '../components/BasicNavBar.vue';

export default {
  name: 'BasicNavBarContainer',

  components: { BasicNavBar },

  mixins: [tokenUserMixin],

  computed: {
    isLoggedIn() {
      return !!this.accessToken;
    },
  },
};
</script>
