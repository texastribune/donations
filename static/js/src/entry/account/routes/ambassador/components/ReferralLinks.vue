<template>
  <ul class="c-ambassador-socials">
    <li>
      <a
        ga-on="click"
        href="#"
        :ga-event-category="ga.tribuneAmbassadors.category"
        :ga-event-action="ga.tribuneAmbassadors.actions.twitter"
        :ga-event-label="ga.tribuneAmbassadors.labels.ambassador"
      >
        Twitter
      </a>
    </li>
    <li>
      <a
        ga-on="click"
        href="#"
        :ga-event-category="ga.tribuneAmbassadors.category"
        :ga-event-action="ga.tribuneAmbassadors.actions.facebook"
        :ga-event-label="ga.tribuneAmbassadors.labels.ambassador"
      >
        Facebook
      </a>
    </li>
    <li>
      <a
        ga-on="click"
        href="#"
        :ga-event-category="ga.tribuneAmbassadors.category"
        :ga-event-action="ga.tribuneAmbassadors.actions.email"
        :ga-event-label="ga.tribuneAmbassadors.labels.ambassador"
      >
        Email
      </a>
    </li>
  </ul>
</template>

<script>
export default {
  name: 'ReferralLinks',
};
</script>
