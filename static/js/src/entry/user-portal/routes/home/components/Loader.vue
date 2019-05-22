<template>
  <div
    class="c-full-page-loader"
    :class="{ 'c-full-page-loader--opaque': display.isOpaque }"
  >
    <div class="l-align-center-y"><div class="c-loading c-loading--s" /></div>
  </div>
</template>

<script>
export default {
  name: 'Loader',

  props: {
    display: {
      type: Object,
      default: () => ({ isOpaque: false }),
    },
  },
};
</script>
