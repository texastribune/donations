<template>
  <user-nav-container v-slot="slotProps">
    <site-footer
      show-home-link
      show-edit-contact-info-link
      show-ambassador-link
      :user-fetch-complete="slotProps.userFetchComplete"
      :show-blast-links="slotProps.showBlastLinks"
      :show-membership-link="slotProps.showMembershipLink"
      :show-payments-link="slotProps.showPaymentsLink"
    />
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
