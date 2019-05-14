<template>
  <aside
    v-if="shouldShow"
    class="c-temp-messages__message has-bg-white-off has-padding has-xxl-btm-marg"
  >
    <div class="c-temp-messages__top has-xxs-btm-marg">
      <slot name="icon"></slot>
      <h2 class="t-size-m">{{ heading }}</h2>
    </div>
    <slot name="content"></slot>
    <button
      class="c-temp-messages__close has-bg-white has-text-gray"
      aria-label="close"
      @click="close"
    >
      <icon name="close" size="m" />
    </button>
  </aside>
</template>

<script>
import Icon from '../../../components/Icon.vue';

export default {
  name: 'Message',

  components: { Icon },

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
