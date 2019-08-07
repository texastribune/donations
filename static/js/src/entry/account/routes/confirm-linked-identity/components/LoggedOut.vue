<template>
  <div>
    <h1 class="has-xl-btm-marg">To verify, please log in</h1>
    <p class="has-b-btm-marg">
      To link <strong>{{ emailToLink }}</strong> to the Texas Tribune account
      created with <strong>{{ existingEmail }}</strong
      >, please log into your account.
    </p>
    <p>
      If you don't own both of the above email addresses, or you didn't mean to
      do this, click <strong>CANCEL</strong> or simply ignore this.
    </p>
    <button @click="onLogIn">Log in</button>
    <button @click="onCancel">Cancel</button>
  </div>
</template>

<script>
export default {
  name: 'ConfirmLinkedIdentityLoggedOut',

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
    },

    onLogIn() {
      this.$emit('logIn');
    },
  },
};
</script>
