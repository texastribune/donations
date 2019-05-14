<template>
  <section class="c-summary-box">
    <div class="c-summary-box__top">
      <h2 class="t-uppercase t-size-m has-m-btm-marg">{{ heading }}</h2>
      <div class="has-xl-btm-marg"><slot name="content"></slot></div>
      <slot name="links"></slot>
    </div>
    <div v-if="!!$slots.bottom" class="c-summary-box__bottom">
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
  },
};
</script>
