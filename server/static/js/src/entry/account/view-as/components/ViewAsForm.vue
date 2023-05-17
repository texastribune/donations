<template>
  <aside
    v-if="isVisible"
    class="c-view-as"
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
export default {
  name: 'ViewAsForm',

  data() {
    return { email: '', isVisible: true };
  },

  methods: {
    submit() {
      this.$router.push({ name: 'accountOverview' });
      this.$emit('doViewAs', this.email);
    },

    reset() {
      this.$router.push({ name: 'accountOverview' });
      this.email = '';
      this.$emit('undoViewAs');
    },

    close() {
      this.isVisible = false;
    },
  },
};
</script>
