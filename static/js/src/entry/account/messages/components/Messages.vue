<template>
  <div
    v-if="numMessagesSeen !== numMessages"
    class="c-messages has-xxl-btm-marg has-ump-side-padding"
  >
    <slot name="messages" :setMessageSeen="setMessageSeen"></slot>
  </div>
</template>

<script>
export default {
  name: 'Messages',

  props: {
    numMessages: {
      type: Number,
      required: true,
    },
  },

  data() {
    return { numMessagesSeen: 0 };
  },

  methods: {
    setMessageSeen() {
      this.numMessagesSeen += 1;
    },
  },
};
</script>
