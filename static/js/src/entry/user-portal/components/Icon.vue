<template>
  <span class="c-icon" :class="`t-size-${display.size}`">
    <svg aria-hidden="true"><use :xlink:href="`#${name}`" /></svg>
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
      default: () => ({ size: 'b' }),
    },
  },
};
</script>
