<template>
  <section
    class="c-summary-boxes__box"
    :class="{ 'is-expired': display.isExpired }"
  >
    <div class="c-summary-boxes__top">
      <h2 class="t-uppercase t-size-m has-m-btm-marg">{{ heading }}</h2>
      <div class="has-xxl-btm-marg"><slot name="content"></slot></div>
      <slot name="links"></slot>
    </div>
    <div
      v-if="!!$slots.bottom"
      class="c-summary-boxes__bottom is-hidden-from-bp-s"
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
