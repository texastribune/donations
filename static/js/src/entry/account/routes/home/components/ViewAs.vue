<template>
  <aside
    v-if="isVisible"
    style="
      position: fixed;
      bottom: 100px;
      left: 0;
      background: rgba(255, 255, 255, 0.9);
      padding: 30px;
      border: 1px solid #ffc200;
    "
  >
    <form @submit.prevent>
      <p
        style="
          margin-bottom: 10px;
        "
      >
        Enter a member's email address
      </p>
      <input
        v-model="email"
        type="email"
        style="
          display: block;
          width: 100%;
          margin-bottom: 10px;
        "
      />
      <button
        type="button"
        style="
          margin-right: 10px;
          padding: 10px;
          background: #dcdcdc;
        "
        :disabled="!allowSubmit"
        @click="submit"
      >
        View as
      </button>
      <button
        type="button"
        style="
          margin-right: 10px;
          padding: 10px;
          background: #dcdcdc;
        "
        @click="reset"
      >
        Reset
      </button>
      <button
        type="button"
        style="
          padding: 10px;
          background: #dcdcdc;
        "
        @click="close"
      >
        Close
      </button>
    </form>
  </aside>
</template>

<script>
/*
 We disable the submit button after it's clicked
 (and re-enable it after someone resets) so the store
 value of context.isViewingAs toggles from false to true
 every time an email address is entered.

 This is so the watcher in ContactInfoContainer knows to
 re-format the data. We have to mangle it differently
 depending whether you're "viewing as," so we have to be
 very explicit about when to update it.
*/

export default {
  name: 'ViewAs',

  data() {
    return { email: '', isVisible: true, allowSubmit: true };
  },

  methods: {
    submit() {
      this.$router.push({ name: 'home' });
      this.allowSubmit = false;
      this.$emit('doViewAs', this.email);
    },

    reset() {
      this.$router.push({ name: 'home' });
      this.email = '';
      this.$emit('undoViewAs', () => {
        this.allowSubmit = true;
      });
    },

    close() {
      this.isVisible = false;
      this.reset();
    },
  },
};
</script>
