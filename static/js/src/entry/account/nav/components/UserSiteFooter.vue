<template>
  <user-provider
    v-slot="{ user: { isBlastSubscriber, hasGivenNotCustom, isNeverGiven } }"
  >
    <site-footer
      show-user-links
      :show-blast-links="!routeIsFetching && isBlastSubscriber"
      :show-membership-link="!routeIsFetching && hasGivenNotCustom"
      :show-payments-link="!routeIsFetching && !isNeverGiven"
    />
  </user-provider>
</template>

<script>
import UserProvider from '../../store/user/Provider.vue';
import SiteFooter from './SiteFooter.vue';

export default {
  name: 'UserSiteFooter',

  components: { UserProvider, SiteFooter },

  props: {
    routeIsFetching: {
      type: Boolean,
      required: true,
    },
  },
};
</script>
