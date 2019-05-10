<template>
  <span class="c-icon" :class="`t-size-${size}`">
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

    size: {
      type: String,
      default: 'b',
    },
  },
};
</script>
