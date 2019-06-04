<template>
  <aside v-if="shouldShow" class="c-message has-bg-white-off">
    <div class="c-message__top has-xxs-btm-marg">
      <slot name="icon"></slot>
      <h2 class="t-size-s">{{ heading }}</h2>
    </div>

    <slot name="content"></slot>

    <button
      class="c-message__close has-bg-white has-text-gray"
      aria-label="close"
      @click="close"
    >
      <icon name="close" :display="{ size: 's', color: 'gray' }" />
    </button>
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
    return { shouldShow: false };
  },

  mounted() {
    if (this.getFromStorage() !== 'true') {
      this.shouldShow = true;
    } else {
      this.$emit('setMessageSeen');
    }
  },

  methods: {
    close() {
      this.shouldShow = false;
      this.setInStorage();
      this.$emit('setMessageSeen');
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
