<template>
  <user-provider v-slot="{ user: { isCustomDonor } }">
    <aside v-if="isCustomDonor" class="c-detail-box">
      <h2 class="t-size-b t-uppercase has-xxxs-btm-marg">Thank you!</h2>
      <p class="has-text-gray-dark t-links-underlined">
        Thank you for your commitment to provide backing for the vital work of
        our journalists. Your support provides a public service to all Wacoans
        &mdash; through our free website, syndication and informative public
        events &mdash; giving Wacoans access to nonpartisan news and information.
        <a
          href="https://support.wacobridge.org/members"
          ga-on="click"
          :ga-event-category="ga.userPortalNav.category"
          :ga-event-action="ga.userPortalNav.actions.inline"
          :ga-event-label="ga.userPortalNav.labels['donor-wall']"
          >Click here</a
        >
        to see other outstanding community members who are supporting the
        Bridge.
      </p>
    </aside>
  </user-provider>
</template>

<script>
import UserProvider from '../../store/user/Provider.vue';

export default {
  name: 'CustomAppeal',

  components: { UserProvider },
};
</script>
