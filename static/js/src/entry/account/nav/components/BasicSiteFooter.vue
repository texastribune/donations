<template>
  <token-user-nav-provider v-slot="slotProps">
    <site-footer
      :show-home-link="false"
      :show-edit-contact-info-link="false"
      :show-ambassador-link="false"
      :show-blast-links="false"
      :show-membership-link="false"
      :show-payments-link="false"
    />
  </token-user-nav-provider>
</template>

<script>
import TokenUserNavProvider from '../providers/TokenUserNavProvider.vue';
import SiteFooter from './SiteFooter.vue';

export default {
  name: 'BasicSiteFooter',

  components: { TokenUserNavProvider, SiteFooter },
};
</script>
