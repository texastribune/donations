<template>
  <div>
    <routes-nav-bar />
    <main class="has-bg-white-off">
      <div class="l-ump-container l-align-center-x">
        <div class="l-ump-grid">
          <div class="l-ump-grid__side is-hidden-until-bp-l">
            <user-nav-container>
              <template v-slot="slotProps">
                <side-nav
                  :user-is-fetching="slotProps.userIsFetching"
                  :show-home-link="slotProps.showHomeLink"
                  :show-blast-links="slotProps.showBlastLinks"
                  :show-membership-link="slotProps.showMembershipLink"
                  :show-payments-link="slotProps.showPaymentsLink"
                />
              </template>
            </user-nav-container>
          </div>
          <div class="l-ump-grid__content has-bg-white">
            <router-view :parent-route-is-fetching="routeIsFetching" />
          </div>
        </div>
      </div>
    </main>
    <view-as />
    <routes-site-footer />
  </div>
</template>

<script>
import routeMixin from '../../mixins/route';
import userMixin from '../../store/user/mixin';
import UserNavContainer from '../../nav/containers/UserNavContainer.vue';
import SideNav from './components/SideNav.vue';

const ViewAs = () =>
  import(/* webpackChunkName: "view-as" */ './containers/ViewAsContainer.vue');

export default {
  name: 'HomeRoute',

  components: { UserNavContainer, SideNav, ViewAs },

  mixins: [routeMixin, userMixin],

  methods: {
    fetchData() {
      return this.getUser();
    },
  },
};
</script>
