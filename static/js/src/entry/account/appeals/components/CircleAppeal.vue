<template>
  <user-provider v-slot="{ user: { isCircleDonor } }">
    <aside v-if="isCircleDonor" class="c-detail-box">
      <h2 class="t-size-b t-uppercase has-xxxs-btm-marg">Thank you!</h2>
      <p class="has-text-gray-dark t-links-underlined">
        Thank you for your commitment to provide backing for the vital work of
        our journalists. Circle Members believe in supporting our mission as a
        public service &mdash; through our free website, syndication and
        informative public events &mdash; so all Texans have access to
        nonpartisan news and information.
        <a
          ga-on="click"
          :href="urls.circle"
          :ga-event-category="ga.userPortalNav.category"
          :ga-event-action="ga.userPortalNav.actions.inline"
          :ga-event-label="ga.userPortalNav.labels['circle-landing']"
        >
          Click here
        </a>
        to see other outstanding community members who are supporting the
        Tribune as Circle Members.
      </p>
    </aside>
  </user-provider>
</template>

<script>
import UserProvider from '../../store/user/Provider.vue';

export default {
  name: 'CircleAppeal',

  components: { UserProvider },
};
</script>
