<template>
  <aside v-if="shouldShow">
    <h2>{{ heading }}</h2>
    <slot></slot> <button @click="close">Close</button>
  </aside>
</template>

<script>
export default {
  name: 'Message',

  props: {
    heading: {
      type: String,
      required: true,
    },

    name: {
      type: String,
      required: true,
    },
  },

  data() {
    return {
      shouldShow: this.getFromStorage() !== 'true',
    };
  },

  methods: {
    close() {
      this.shouldShow = false;
      this.setInStorage();
    },

    getFromStorage() {
      return localStorage.getItem(`${this.name}Seen`);
    },

    setInStorage() {
      localStorage.setItem(`${this.name}Seen`, true);
    },
  },
};
</script>
