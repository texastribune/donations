<template>
  <section
    class="c-summary-box has-bg-white"
    :class="{
      'is-expired': mergedDisplay.isExpired,
      'c-summary-box--has-btm':
        !!$slots.bottom && !mergedDisplay.hasMobileBottom,
    }"
  >
    <div class="c-summary-box__top">
      <h2 class="t-uppercase t-size-b has-s-btm-marg">{{ heading }}</h2>
      <div class="has-xxl-btm-marg"><slot name="content"></slot></div>
      <div class="t-links-underlined"><slot name="links"></slot></div>
    </div>
    <div
      v-if="!!$slots.bottom"
      class="c-summary-box__bottom"
      :class="{ 'is-hidden-from-bp-s': mergedDisplay.hasMobileBottom }"
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
      default: () => ({}),
    },
  },

  computed: {
    mergedDisplay() {
      return { isExpired: false, hasMobileBottom: true, ...this.display };
    },
  },
};
</script>
