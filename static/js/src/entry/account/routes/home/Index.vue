<template>
  <div>
    <nav-bar :show-route-links="!routeIsFetching" />

    <main class="has-bg-white-off">
      <div class="l-ump-container l-align-center-x">
        <div class="l-ump-grid">
          <div class="l-ump-grid__side is-hidden-until-bp-l">
            <side-nav :show-route-links="!routeIsFetching" />
          </div>
          <div class="l-ump-grid__content has-bg-white">
            <router-view :parent-route-is-fetching="routeIsFetching" />
          </div>
        </div>
      </div>
    </main>

    <view-as v-if="!routeIsFetching" />
    <site-footer :show-route-links="!routeIsFetching" />
  </div>
</template>

<script>
import routeMixin from '../../mixins/route';
import userMixin from './mixins/user';
import SideNav from './containers/SideNavContainer.vue';

const ViewAs = () =>
  import(/* webpackChunkName: "view-as" */ './containers/ViewAsContainer.vue');

export default {
  name: 'HomeRoute',

  components: { SideNav, ViewAs },

  mixins: [routeMixin, userMixin],

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
    fetchData() {
      return this.getUser();
    },
  },
};
</script>
