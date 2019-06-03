<template>
  <div>
    <nav-bar />
    <main class="has-bg-white-off">
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
import protectedRouteMixin from '../../mixins/protected-route';
import NavBar from '../../components/NavBar.vue';
import SideNav from './components/SideNav.vue';

export default {
  name: 'Index',

  components: { SideNav, NavBar },

  mixins: [protectedRouteMixin],
};
</script>
