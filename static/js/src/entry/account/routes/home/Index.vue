<template>
  <loader v-if="isFetching">
    <template v-slot:text>
      Hold tight, we're grabbing your account information
    </template>
  </loader>

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
    <view-as />
    <site-footer />
  </div>
</template>

<script>
import { mapActions } from 'vuex';

import routeMixin from '../../mixins/route';
import SideNav from './containers/SideNavContainer.vue';
import ViewAs from './containers/ViewAsContainer.vue';

export default {
  name: 'HomeRoute',

  components: { SideNav, ViewAs },

  mixins: [routeMixin],

  computed: {
    route() {
      return {
        isExact: false,
        isProtected: true,
        meetsCriteria: true,
        title: null,
      };
    },
  },

  methods: {
    ...mapActions('user', ['getUser']),

    async fetchData() {
      return this.getUser();
    },
  },
};
</script>
