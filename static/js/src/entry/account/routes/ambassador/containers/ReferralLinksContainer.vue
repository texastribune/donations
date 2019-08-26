<template>
  <referral-links :twitter-url="twitterUrl" :facebook-url="facebookUrl" />
</template>

<script>
import userMixin from '../../../store/user/mixin';
import ReferralLinks from '../components/ReferralLinks.vue';

export default {
  name: 'ReferralLinksContainer',

  components: { ReferralLinks },

  mixins: [userMixin],

  computed: {
    twitterUrl() {
      return this.user.twitter;
    },

    facebookUrl() {
      return this.user.facebook;
    },
  },
};
</script>
