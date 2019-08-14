<template>
  <div>
    <h1 class="has-xl-btm-marg">Are you sure?</h1>
    <p class="has-b-btm-marg">
      You're about to link <strong>{{ emailToLink }}</strong> to Texas Tribune
      account: <strong>{{ existingEmail }}</strong
      >. Click below to confirm this update to your account.
    </p>
    <p class="has-xl-btm-marg">
      If these email addresses don't belong to you, or you didn't mean to do
      this, click <strong>CANCEL</strong> or simply ignore this.
    </p>
    <div class="c-btn-or-btn">
      <div class="c-btn-or-btn__first">
        <base-button
          :display="{ bg: 'gray-light', color: 'black' }"
          text="Confirm email link"
          @onClick="onConfirm"
        />
      </div>
      <span class="c-btn-or-btn__word t-align-center l-align-center-self"
        >or</span
      >
      <div class="c-btn-or-btn__last">
        <base-button
          :display="{ bg: 'gray-light', color: 'black' }"
          text="Cancel"
          @onClick="onCancel"
        />
      </div>
    </div>
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
    onConfirm() {
      this.$emit('confirm');

      window.dataLayer.push({
        event: this.ga.customEventName,
        gaCategory: this.ga.userPortal.category,
        gaAction: this.ga.userPortal.actions['confirm-linked-email'],
        gaLabel: this.ga.userPortal.labels['confirm-linked-identity'],
      });
    },

    onCancel() {
      this.$emit('goHome');

      window.dataLayer.push({
        event: this.ga.customEventName,
        gaCategory: this.ga.userPortal.category,
        gaAction: this.ga.userPortal.actions['cancel-linked-email'],
        gaLabel: this.ga.userPortal.labels['confirm-linked-identity'],
      });
    },
  },
};
</script>
