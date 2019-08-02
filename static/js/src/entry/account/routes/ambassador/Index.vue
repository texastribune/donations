<template>
  <route-loader v-if="routeIsFetching">
    <template v-slot:text>
      Grabbing your ambassador information
    </template>
  </route-loader>

  <div v-else>
    <h1
      class="has-ump-top-padding has-ump-side-padding has-l-btm-marg t-size-xl"
    >
      Your Referrals
    </h1>

    <div class="has-ump-side-padding has-xxl-btm-marg">
      <p class="has-xxl-btm-marg t-size-b t-space-heading-m">
        Thank you for being a Texas Tribune member! You can help ensure the rest
        of Texas knows about our mission to inform and engage the public in
        politics and policy news by sharing your membership story.
      </p>
      <referral-links />
    </div>

    <help ambassador />
  </div>
</template>

<script>
import routeMixin from '../../mixins/route';
import RouteLoader from '../home/components/RouteLoader.vue';
import Help from '../home/components/Help.vue';
import ReferralLinks from './components/ReferralLinks.vue';

export default {
  name: 'AmbassadorRoute',

  components: { Help, RouteLoader, ReferralLinks },

  mixins: [routeMixin],
};
</script>
