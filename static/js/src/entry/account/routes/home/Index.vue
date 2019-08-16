<template>
  <div>
    <routes-nav-bar />

    <main class="has-bg-white-off">
      <div class="l-ump-container l-align-center-x">
        <div class="l-ump-grid">
          <div class="l-ump-grid__side is-hidden-until-bp-l">
            <user-nav-container v-slot="slotProps">
              <side-nav
                show-home-link
                show-edit-contact-info-link
                show-ambassador-link
                :user-fetch-complete="slotProps.userFetchComplete"
                :show-blast-link="slotProps.showBlastLinks"
                :show-membership-link="slotProps.showMembershipLink"
                :show-payments-link="slotProps.showPaymentsLink"
              />
            </user-nav-container>
          </div>
          <div class="l-ump-grid__content has-bg-white">
            <router-view :parent-route-is-fetching="routeIsFetching" />
          </div>
        </div>
      </div>
    </main>

    <routes-site-footer />

    <view-as />
  </div>
</template>

<script>
import routeMixin from '../mixin';
import userMixin from '../../store/user/mixin';
import UserNavContainer from '../../nav/containers/UserNavContainer.vue';
import SideNav from './components/SideNav.vue';

const ViewAs = () =>
  import(/* webpackChunkName: "view-as" */ './containers/ViewAsContainer.vue');

export default {
  name: 'HomeRoute',

  components: { UserNavContainer, SideNav, ViewAs },

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
