<template>
  <site-footer :show-route-links="showRouteLinks" :user="user" />
</template>

<script>
import SiteFooter from '../components/SiteFooter.vue';
import userMixin from '../routes/home/mixins/user';

export default {
  name: 'SiteFooterContainer',

  components: { SiteFooter },

  mixins: [userMixin],

  props: {
    showRouteLinks: {
      type: Boolean,
      default: true,
    },
  },
};
</script>
