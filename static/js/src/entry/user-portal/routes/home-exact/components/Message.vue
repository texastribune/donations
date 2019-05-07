<template>
  <aside v-if="shouldShow">
    <button @click="close">Close</button> <slot></slot>
  </aside>
</template>

<script>
export default {
  name: 'Message',

  props: {
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
