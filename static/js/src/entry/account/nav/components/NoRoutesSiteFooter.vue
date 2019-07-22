<template>
  <user-nav-container>
    <template v-slot="slotProps">
      <site-footer
        user-fetch-complete
        :show-home-link="false"
        :show-edit-contact-info-link="false"
        :show-blast-links="false"
        :show-membership-link="false"
        :show-payments-link="false"
      />
    </template>
  </user-nav-container>
</template>

<script>
import UserNavContainer from '../containers/UserNavContainer.vue';
import SiteFooter from './SiteFooter.vue';

export default {
  name: 'NoRoutesSiteFooter',

  components: { UserNavContainer, SiteFooter },
};
</script>
