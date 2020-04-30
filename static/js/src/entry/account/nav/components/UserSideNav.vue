<template>
  <user-provider
    v-slot="{ user: { isBlastSubscriber, hasGivenNotCustom, isNeverGiven } }"
  >
    <side-nav
      :show-blast-link="isBlastSubscriber"
      :show-membership-link="hasGivenNotCustom"
      :show-payments-link="!isNeverGiven"
    />
  </user-provider>
</template>

<script>
import UserProvider from '../../store/user/Provider.vue';

import SideNav from './SideNav.vue';

export default {
  name: 'UserSideNav',

  components: { UserProvider, SideNav },
};
</script>
