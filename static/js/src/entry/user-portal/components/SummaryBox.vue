<template>
  <section class="c-summary-box">
    <h2>{{ heading }}</h2>
    <slot name="content"></slot> <slot name="links"></slot>
    <div v-if="!!$slots.bottom" class=""><slot name="bottom"></slot></div>
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
