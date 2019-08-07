<template>
  <div>
    <h1 class="has-xl-btm-marg">Are you sure?</h1>
    <p class="has-b-btm-marg">
      You're about to link <strong>{{ emailToLink }}</strong> to your Texas
      Tribune account with email <strong>{{ existingEmail }}</strong
      >.
    </p>
    <p>
      If you don't own both of the above email addresses, or you didn't mean to
      do this, click <strong>CANCEL</strong>.
    </p>
    <button @click="onCancel">Cancel</button>
    <button @click="onConfirm">Yes, link emails</button>
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

  methods: {
    onCancel() {
      this.$emit('goHome');

      window.dataLayer.push({
        event: this.ga.customEventName,
        gaCategory: this.ga.userPortal.category,
        gaAction: this.ga.userPortal.actions['cancel-linked-email'],
        gaLabel: this.ga.userPortal.labels['confirm-linked-identity'],
      });
    },

    onConfirm() {
      this.$emit('confirm');

      window.dataLayer.push({
        event: this.ga.customEventName,
        gaCategory: this.ga.userPortal.category,
        gaAction: this.ga.userPortal.actions['confirm-linked-email'],
        gaLabel: this.ga.userPortal.labels['confirm-linked-identity'],
      });
    },
  },
};
</script>
