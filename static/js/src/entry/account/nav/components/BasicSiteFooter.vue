<template>
  <site-footer :show-user-links="false" />
</template>

<script>
import SiteFooter from './SiteFooter.vue';

export default {
  name: 'BasicSiteFooter',

  components: { SiteFooter },
};
</script>
