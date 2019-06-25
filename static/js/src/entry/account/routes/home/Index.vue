<template>
  <div>
    <loader v-if="isFetching">
      <template v-slot:text>
        Hold tight, we're grabbing your account information
      </template>
    </loader>

    <nav-bar v-if="!isFetching" />

    <main class="has-bg-white-off">
      <div class="l-ump-container l-align-center-x">
        <div class="l-ump-grid">
          <div class="l-ump-grid__side is-hidden-until-bp-l">
            <side-nav v-if="!isFetching" />
          </div>
          <div class="l-ump-grid__content has-bg-white">
            <router-view :parent-is-fetching="isFetching" />
          </div>
        </div>
      </div>
    </main>

    <view-as v-if="!isFetching" />

    <site-footer v-if="!isFetching" />
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
        title: null,
      };
    },
  },

  methods: {
    ...mapActions('user', ['getUser']),

    fetchData() {
      return this.getUser();
    },
  },
};
</script>
