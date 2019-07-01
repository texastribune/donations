<template>
  <section
    class="c-summary-box has-bg-white"
    :class="{ 'is-expired': display.isExpired }"
  >
    <div class="c-summary-box__top">
      <h2 class="t-uppercase t-size-b has-s-btm-marg">{{ heading }}</h2>
      <div class="has-xxl-btm-marg"><slot name="content"></slot></div>
      <div class="t-linkstyle--underlined"><slot name="links"></slot></div>
    </div>
    <div
      v-if="!!$slots.bottom"
      class="c-summary-box__bottom is-hidden-from-bp-s"
    >
      <slot name="bottom"></slot>
    </div>
  </section>
</template>

<script>
export default {
  name: 'SummaryBox',

  props: {
    heading: {
      type: String,
      required: true,
    },

    display: {
      type: Object,
      default: () => ({ isExpired: false }),
    },
  },
};
</script>
