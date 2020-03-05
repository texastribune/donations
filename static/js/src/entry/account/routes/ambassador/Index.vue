<template>
  <div>
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

      <internal-nav />
    </div>

    <contact-us :ga-label="ga.userPortal.labels.ambassador">
      <template v-slot:text>
        Have questions about your account? Or feedback about this website? Email
      </template>
    </contact-us>
  </div>
</template>

<script>
import routeMixin from '../mixin';

import ReferralForm from './containers/ReferralFormContainer.vue';

import ContactUs from '../../components/ContactUs.vue';
import ReferralLinks from './components/ReferralLinks.vue';
import InternalNav from './components/InternalNav.vue';

export default {
  name: 'AmbassadorRoute',

  components: { ContactUs, ReferralLinks, ReferralForm, InternalNav },

  mixins: [routeMixin],
};
</script>
