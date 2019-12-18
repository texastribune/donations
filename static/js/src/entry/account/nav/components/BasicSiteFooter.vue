<template>
  <token-user-nav-provider v-slot="slotProps">
    <site-footer :show-user-links="false" />
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
