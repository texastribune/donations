<template>
  <div class="c-full-page-loader">
    <div class="l-align-center-y has-xl-padding">
      <div class="c-loading c-loading--tight has-b-btm-marg" />
      <p class="has-text-gray t-align-center t-size-m">
        <strong><slot name="text"></slot></strong>
      </p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Loader',
};
</script>
