<template>
  <loader v-if="!canAccess" :display="{ isOpaque: true }" />
  <div v-else>
    <nav style="height:45px;background:#fff;border-bottom:1px solid #dcdcdc;" />
    <main class="has-bg-white-off">
      <button @click="user.logOut()">Log out</button>
      <div class="l-ump-container l-align-center-x">
        <div class="l-ump-grid">
          <div class="l-ump-grid__side is-hidden-until-bp-l"><side-nav /></div>
          <div class="l-ump-grid__content"><router-view /></div>
        </div>
      </div>
    </main>
    <site-footer />
  </div>
</template>

<script>
import userMixin from '../../mixins/user';
import store from '../../store';
import { logIn } from '../../utils/auth-actions';
import SideNav from './components/SideNav.vue';

export default {
  name: 'Index',

  components: { SideNav },

  mixins: [userMixin],

  data() {
    return { canAccess: false };
  },

  mounted() {
    this.redirectIfLoggedOut();
  },

  methods: {
    redirectIfLoggedOut() {
      if (!store.state.user.idToken) logIn();
      else this.canAccess = true;
    },
  },
};
</script>
