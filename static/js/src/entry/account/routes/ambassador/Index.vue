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

    <div class="has-ump-side-padding has-xxxl-btm-marg">
      <p class="has-xl-btm-marg has-text-gray-dark t-size-s t-space-heading-m">
        Thank you for being a Texas Tribune member! You can help ensure the rest
        of Texas knows about our mission to inform and engage the public in
        politics and policy news by sharing your membership story.
      </p>
      <section class="has-xl-btm-marg">
        <h2 class="has-s-btm-marg t-size-m">
          Why do you support The Texas Tribune?
        </h2>
        <div class="has-xl-btm-marg"><referral-links /></div>
        <referral-form />
      </section>
      <links />
    </div>

    <help ambassador />
  </div>
</template>

<script>
import routeMixin from '../../mixins/route';
import RouteLoader from '../home/components/RouteLoader.vue';
import Help from '../home/components/Help.vue';
import ReferralLinks from './components/ReferralLinks.vue';
import ReferralForm from './containers/ReferralFormContainer.vue';
import Links from './containers/LinksContainer.vue';

export default {
  name: 'AmbassadorRoute',

  components: { Help, RouteLoader, ReferralLinks, ReferralForm, Links },

  mixins: [routeMixin],

  data() {
    return { title: 'Tribune Ambassadors' };
  },
};
</script>
