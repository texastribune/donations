<template>
  <user-internal-nav
    show-reset-pw
    show-membership-status
    show-blast-subscription
    :pw-reset-ga-label="ga.userPortal.labels['edit-contact-info']"
  />
</template>

<script>
export default {
  name: 'EditContactInfoInternalNav',
};
</script>
