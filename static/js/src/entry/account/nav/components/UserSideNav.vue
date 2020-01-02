<template>
  <user-provider
    v-slot="{ isBlastSubscriber, hasGivenNotCustom, isNeverGiven }"
  >
    <side-nav
      :show-blast-link="!routeIsFetching && isBlastSubscriber"
      :show-membership-link="!routeIsFetching && hasGivenNotCustom"
      :show-payments-link="!routeIsFetching && !isNeverGiven"
    />
  </user-provider>
</template>

<script>
import UserProvider from '../../store/user/Provider.vue';
import SideNav from './SideNav.vue';

export default {
  name: 'UserSideNav',

  components: { UserProvider, SideNav },

  props: {
    routeIsFetching: {
      type: Boolean,
      required: true,
    },
  },
};
</script>
