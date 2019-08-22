<template>
  <ul class="c-ambassador-socials">
    <li class="has-s-btm-marg">
      <a
        ga-on="click"
        href="https://twitter.com/intent/tweet?url=https%3A%2F%2Fsupport.texastribune.org%2Fdonate%3Fcode%3Dump-1%26campaignId%3D7010f0000013I2yAAE%26utm_campaign%3Dtrib-marketing%26utm_content%3Dump-share%26referralId%3D003S000001AoQTVIA3&amp;text=%23ISupportTexasTribune%20because%20"
        class="c-button c-button--s has-text-white has-bg-twitter has-padding l-width-full l-display-block"
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
        href="https://www.facebook.com/sharer/sharer.php?u=https%3A%2F%2Fsupport.texastribune.org%2Fdonate%3Fcode%3Dump-1%26campaignId%3D7010f0000013I2yAAE%26utm_campaign%3Dtrib-marketing%26utm_content%3Dump-share%26referralId%3D003S000001AoQTVIA3"
        class="c-button c-button--s has-text-white has-bg-facebook has-padding l-width-full l-display-block"
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
};
</script>
