<template>
  <div>
    <user-nav-bar :route-is-fetching="routeIsFetching" />

    <main class="has-bg-white-off">
      <div class="l-ump-container l-align-center-x">
        <div class="l-ump-grid">
          <div class="l-ump-grid__side is-hidden-until-bp-l">
            <user-side-nav :route-is-fetching="routeIsFetching" />
          </div>
          <div class="l-ump-grid__content has-bg-white">
            <router-view :parent-route-is-fetching="routeIsFetching" />
          </div>
        </div>
      </div>
    </main>

    <user-site-footer :route-is-fetching="routeIsFetching" />

    <view-as />
  </div>
</template>

<script>
import routeMixin from '../mixin';
import userMixin from '../../store/user/mixin';
import UserSideNav from '../../nav/components/UserSideNav.vue';

const ViewAs = () =>
  import(/* webpackChunkName: "view-as" */ './containers/ViewAsContainer.vue');

export default {
  name: 'HomeRoute',

  components: { UserSideNav, ViewAs },

  mixins: [routeMixin, userMixin],

  data() {
    return { title: null };
  },

  methods: {
    fetchData() {
      return this.getUser();
    },
  },
};
</script>
