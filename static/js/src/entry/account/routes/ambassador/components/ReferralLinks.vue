<template>
  <ul class="c-ambassador-socials">
    <li class="has-s-btm-marg">
      <a
        ga-on="click"
        class="c-button c-button--s has-text-white has-bg-twitter has-padding l-width-full l-display-block"
        :href="twitterUrl"
        :ga-event-category="ga.tribuneAmbassadors.category"
        :ga-event-action="ga.tribuneAmbassadors.actions.twitter"
        :ga-event-label="ga.tribuneAmbassadors.labels.ambassador"
      >
        Tweet #ISupportTexasTribune
      </a>
    </li>
    <li class="has-s-btm-marg">
      <a
        ga-on="click"
        class="c-button c-button--s has-text-white has-bg-facebook has-padding l-width-full l-display-block"
        :href="facebookUrl"
        :ga-event-category="ga.tribuneAmbassadors.category"
        :ga-event-action="ga.tribuneAmbassadors.actions.facebook"
        :ga-event-label="ga.tribuneAmbassadors.labels.ambassador"
      >
        Share on Facebook
      </a>
    </li>
    <li>
      <a
        ga-on="click"
        href="mailto:?subject=Join%20me%20in%20supporting%20journalism%20that%20serves%20all%20Texans&body=As%20a%20member%20of%20The%20Texas%20Tribune%2C%20I'm%20supporting%20nonprofit%2C%20nonpartisan%20reporting%20on%20politics%20and%20policy%20issues%20of%20statewide%20importance.%20Will%20you%20join%20me%20by%20making%20a%20donation%20now%3F%20"
        class="c-button c-button--s has-text-black-off has-bg-gray-light has-padding l-width-full l-display-block"
        :ga-event-category="ga.tribuneAmbassadors.category"
        :ga-event-action="ga.tribuneAmbassadors.actions.email"
        :ga-event-label="ga.tribuneAmbassadors.labels.ambassador"
      >
        Email friends and family
      </a>
    </li>
  </ul>
</template>

<script>
export default {
  name: 'ReferralLinks',

  props: {
    twitterUrl: {
      type: String,
      required: true,
    },

    facebookUrl: {
      type: String,
      required: true,
    },
  },
};
</script>
