<template>
  <span
    class="c-icon"
    :class="`t-size-${mergedDisplay.size} has-text-${mergedDisplay.color}`"
    :style="{ 'font-size': mergedDisplay.inlineSize }"
  >
    <svg aria-hidden="true" focusable="false">
      <use :xlink:href="`#${name}`" />
    </svg>
  </span>
</template>

<script>
export default {
  name: 'Icon',

  props: {
    name: {
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
      return {
        size: 'b',
        color: 'black',
        inlineSize: '',
        ...this.display,
      };
    },
  },
};
</script>
