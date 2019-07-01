<template>
  <aside
    class="c-appeal t-space-heading-m has-ump-side-padding has-white-off-bg-until-bp-l"
  >
    <p class="has-text-gray-dark t-space-heading-m t-linkstyle--underlined">
      Thank you for your commitment to provide backing for the vital work of our
      journalists. Circle Members believe in supporting our mission as a public
      service &mdash; through our free website, syndication and informative
      public events &mdash; so all Texans have access to nonpartisan news and
      information.
      <a
        ga-on="click"
        :href="circleUrl"
        :ga-event-category="ga.userPortalNav.category"
        :ga-event-action="ga.userPortalNav.actions.inline"
        :ga-event-label="ga.userPortalNav.labels['circle-landing']"
      >
        Click here
      </a>
      to see other outstanding community members who are supporting the Tribune
      as Circle Members.
    </p>
  </aside>
</template>

<script>
export default {
  name: 'CircleAppeal',
};
</script>
