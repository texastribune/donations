<template>
  <side-nav :user="user" />
</template>

<script>
import SideNav from '../components/SideNav.vue';
import userMixin from '../../../mixins/user';

export default {
  name: 'SideNavContainer',

  components: { SideNav },

  mixins: [userMixin],
};
</script>
