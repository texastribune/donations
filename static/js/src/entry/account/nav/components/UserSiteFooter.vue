<template>
  <user-nav-provider v-slot="slotProps">
    <site-footer
      show-home-link
      show-edit-contact-info-link
      show-ambassador-link
      :show-blast-links="!routeIsFetching && slotProps.showBlastLinks"
      :show-membership-link="!routeIsFetching && slotProps.showMembershipLink"
      :show-payments-link="!routeIsFetching && slotProps.showPaymentsLink"
    />
  </user-nav-provider>
</template>

<script>
import UserNavProvider from '../providers/UserNavProvider.vue';
import SiteFooter from './SiteFooter.vue';

export default {
  name: 'UserSiteFooter',

  components: { UserNavProvider, SiteFooter },

  props: {
    routeIsFetching: {
      type: Boolean,
      required: true,
    },
  },
};
</script>
