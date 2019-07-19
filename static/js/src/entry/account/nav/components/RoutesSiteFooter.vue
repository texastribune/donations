<template>
  <user-nav-container>
    <template v-slot="slotProps">
      <site-footer
        :user-is-fetching="slotProps.userIsFetching"
        :show-home-link="slotProps.showHomeLink"
        :show-blast-links="slotProps.showBlastLinks"
        :show-membership-link="slotProps.showMembershipLink"
        :show-payments-link="slotProps.showPaymentsLink"
      />
    </template>
  </user-nav-container>
</template>

<script>
import UserNavContainer from '../containers/UserNavContainer.vue';
import SiteFooter from './SiteFooter.vue';

export default {
  name: 'RoutesSiteFooter',

  components: { UserNavContainer, SiteFooter },
};
</script>
