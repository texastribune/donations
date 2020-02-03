<template>
  <user-provider v-slot="{ user: { twitterUrl, facebookUrl, emailUrl } }">
    <ul class="c-ambassador-socials">
      <li class="has-s-btm-marg">
        <a
          ga-on="click"
          class="c-button c-button--s has-text-white has-bg-twitter has-padding l-width-full l-display-block"
          rel="noopener noreferrer"
          target="_blank"
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
          rel="noopener noreferrer"
          target="_blank"
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
          class="c-button c-button--s has-text-black-off has-bg-gray-light has-padding l-width-full l-display-block"
          rel="noopener noreferrer"
          target="_blank"
          :href="emailUrl"
          :ga-event-category="ga.tribuneAmbassadors.category"
          :ga-event-action="ga.tribuneAmbassadors.actions.email"
          :ga-event-label="ga.tribuneAmbassadors.labels.ambassador"
        >
          Email friends and family
        </a>
      </li>
    </ul>
  </user-provider>
</template>

<script>
import UserProvider from '../../../store/user/Provider.vue';

export default {
  name: 'ReferralLinks',

  components: { UserProvider },
};
</script>
