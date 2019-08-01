<template>
  <div>
    <h1 class="has-xl-btm-marg">Are you sure?</h1>
    <p class="t-space-heading-m has-b-btm-marg">
      You're about to link <strong>{{ emailToLink }}</strong> to your Texas
      Tribune account with email <strong>{{ existingEmail }}</strong
      >.
    </p>
    <p class="t-space-heading-m">
      If you don't own both of the above email addresses, or you didn't mean to
      do this, click <strong>CANCEL</strong>.
    </p>
    <button @click="$emit('goHome')">Cancel</button>
    <button @click="$emit('confirm')">Yes, link emails</button>
  </div>
</template>

<script>
export default {
  name: 'ConfirmLinkedIdentityLoggedIn',

  props: {
    existingEmail: {
      type: String,
      required: true,
    },

    emailToLink: {
      type: String,
      required: true,
    },
  },
};
</script>
