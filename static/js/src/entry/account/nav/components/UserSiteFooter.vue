<template>
  <user-provider
    v-slot="{ user: { isBlastSubscriber, hasGivenNotCustom, isNeverGiven } }"
  >
    <site-footer
      show-user-links
      :show-blast-links="isBlastSubscriber"
      :show-membership-link="hasGivenNotCustom"
      :show-payments-link="!isNeverGiven"
    />
  </user-provider>
</template>

<script>
import UserProvider from '../../store/user/Provider.vue';

import SiteFooter from './SiteFooter.vue';

export default {
  name: 'UserSiteFooter',

  components: { UserProvider, SiteFooter },
};
</script>
