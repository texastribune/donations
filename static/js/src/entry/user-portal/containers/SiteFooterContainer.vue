<template>
  <site-footer :show-route-links="showRouteLinks" />
</template>

<script>
import SiteFooter from '../components/SiteFooter.vue';

export default {
  name: 'SiteFooterContainer',

  components: { SiteFooter },

  props: {
    showRouteLinks: {
      type: Boolean,
      default: true,
    },
  },
};
</script>
