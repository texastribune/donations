<template>
  <side-nav :user="user" />
</template>

<script>
import SideNav from '../components/SideNav.vue';
import userMixin from '../../../mixins/user';

export default {
  name: 'NavBarContainer',

  components: { SideNav },

  mixins: [userMixin],
};
</script>
