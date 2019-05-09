<template>
  <span class="c-icon">
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
  },
};
</script>
