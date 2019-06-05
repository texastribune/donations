<template>
  <loader v-if="isFetching" />
  <div v-else>
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
import { mapActions } from 'vuex';

import protectedRouteMixin from '../../mixins/protected-route';
import routeFetchMixin from '../../mixins/route-fetch';
import SideNav from './components/SideNav.vue';

export default {
  name: 'Index',

  components: { SideNav },

  mixins: [protectedRouteMixin, routeFetchMixin],

  methods: {
    ...mapActions('user', ['getUser']),

    async fetchData() {
      return this.getUser();
    },
  },
};
</script>
