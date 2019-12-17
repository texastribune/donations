<template>
  <user-nav-provider v-slot="slotProps">
    <side-nav
      show-home-link
      show-edit-contact-info-link
      show-ambassador-link
      :show-blast-link="!routeIsFetching && slotProps.showBlastLinks"
      :show-membership-link="!routeIsFetching && slotProps.showMembershipLink"
      :show-payments-link="!routeIsFetching && slotProps.showPaymentsLink"
    />
  </user-nav-provider>
</template>

<script>
import UserNavProvider from '../providers/UserNavProvider.vue';
import SideNav from './SideNav.vue';

export default {
  name: 'UserSideNav',

  components: { UserNavProvider, SideNav },

  props: {
    routeIsFetching: {
      type: Boolean,
      required: true,
    },
  },
};
</script>
