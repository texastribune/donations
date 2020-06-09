<template>
  <aside
    v-if="shouldShow"
    :class="{
      'c-message--on-gray-mobile-bg': mergedDisplay.onGrayMobileBg,
    }"
    class="c-message"
  >
    <div class="c-message__top has-xxs-btm-marg">
      <slot name="icon"></slot>
      <h2 class="t-size-s">{{ heading }}</h2>
    </div>

    <slot name="content"></slot>

    <button
      class="c-message__close has-bg-white has-text-gray"
      aria-label="close message"
      @click="close"
    >
      <icon name="close" :display="{ size: 'xxs', color: 'gray' }" />
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

    gaLabel: {
      type: String,
      required: true,
    },

    display: {
      type: Object,
      default: () => ({}),
    },
  },

  data() {
    return { shouldShow: false };
  },

  computed: {
    mergedDisplay() {
      return { onGrayMobileBg: false, ...this.display };
    },
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

      window.dataLayer.push({
        event: this.ga.customEventName,
        gaCategory: this.ga.userPortal.category,
        gaAction: this.ga.userPortal.actions['clear-notification'],
        gaLabel: this.gaLabel,
      });
    },

    getFromStorage() {
      try {
        return localStorage.getItem(`${this.name}Seen`);
      } catch (err) {
        return 'true';
      }
    },

    setInStorage() {
      localStorage.setItem(`${this.name}Seen`, true);
    },
  },
};
</script>
