<template>
  <user-internal-nav
    show-reset-password
    show-membership-status
    show-blast-subscription
    :password-reset-ga-label="ga.userPortal.labels['edit-contact-info']"
  />
</template>

<script>
export default {
  name: 'EditContactInfoInternalNav',
};
</script>
