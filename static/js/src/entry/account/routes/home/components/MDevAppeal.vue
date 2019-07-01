<template>
  <aside
    class="c-appeal t-space-heading-m has-ump-side-padding has-white-off-bg-until-bp-l"
  >
    <p class="has-text-gray-dark t-space-heading-m t-linkstyle--underlined">
      Thank you for your commitment to provide backing for the vital work of our
      journalists. Your support provides a public service to all Texans &mdash;
      through our free website, syndication and informative public events
      &mdash; giving Texans access to nonpartisan news and information.
      <a
        href="https://www.texastribune.org/support-us/donors-and-members/"
        ga-on="click"
        :ga-event-category="ga.userPortalNav.category"
        :ga-event-action="ga.userPortalNav.actions.inline"
        :ga-event-label="ga.userPortalNav.labels['donor-wall']"
        >Click here</a
      >
      to see other outstanding community members who are supporting the Tribune.
    </p>
  </aside>
</template>

<script>
export default {
  name: 'MDevAppeal',
};
</script>
