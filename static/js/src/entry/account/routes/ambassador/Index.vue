<template>
  <route-loader v-if="routeIsFetching">
    <template v-slot:text>
      Grabbing your referral information
    </template>
  </route-loader>

  <div v-else>
    <h1
      class="has-ump-top-padding has-ump-side-padding has-l-btm-marg t-size-xl"
    >
      Refer a Friend
    </h1>

    <div class="has-ump-side-padding has-xxxl-btm-marg">
      <p class="has-xl-btm-marg has-text-gray-dark t-size-s">
        Thank you for supporting our nonprofit newsroom! Thanks to your support,
        we're hard at work on our mission of informing and engaging Texans on
        politics and policy issues of statewide importance. Did you know that
        recommendations from members like you are our most effective tool for
        reaching readers who haven't yet heard about our journalism? So, what do
        you say: Do we have your endorsement? Tell the rest of Texas why our
        nonpartisan reporting matters to you.
      </p>
      <section class="has-xl-btm-marg">
        <h2 class="has-s-btm-marg t-size-b">
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
import routeMixin from '../mixin';
import RouteLoader from '../home/components/RouteLoader.vue';
import Help from '../home/components/Help.vue';
import ReferralLinks from './containers/ReferralLinksContainer.vue';
import ReferralForm from './containers/ReferralFormContainer.vue';
import Links from './containers/LinksContainer.vue';

export default {
  name: 'AmbassadorRoute',

  components: { Help, RouteLoader, ReferralLinks, ReferralForm, Links },

  mixins: [routeMixin],

  data() {
    return { title: 'Refer a Friend' };
  },
};
</script>
