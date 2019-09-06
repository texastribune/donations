<template>
  <referral-links
    :twitter-url="twitterUrl"
    :facebook-url="facebookUrl"
    :email-url="emailUrl"
  />
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
      return this.user.twitter_share_url;
    },

    facebookUrl() {
      return this.user.facebook_share_url;
    },

    emailUrl() {
      return this.user.email_share_url;
    },
  },
};
</script>
